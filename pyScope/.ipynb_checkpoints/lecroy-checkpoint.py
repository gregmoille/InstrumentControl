import re
import array
import io
import struct
import numpy as np
import socket
import os
import ipdb
import pandas as pd

# data types in lecroy binary blocks, where:
# length  -- byte length of type
# string  -- string representation of type
# packfmt -- format string for struct.unpack()
class String:
    length = 16
    string = 'string'
class Byte:
    length = 1
    string = 'byte'
    packfmt = 'b'
class Word:
    length = 2
    string = 'word'
    packfmt = 'h'
class Long:
    length = 4
    string = 'long'
    packfmt = 'l'
class Enum:
    length = 2
    string = 'enum'
    packfmt = 'h'
class Float:
    length = 4
    string = 'float'
    packfmt = 'f'
class Double:
    length = 8
    string = 'double'
    packfmt = 'd'
class TimeStamp:
    length = 16
    string = 'time_stamp'
    packfmt = 'dbbbbhh'
class UnitDefinition:
    length = 48
    string = 'unit_definition'

# all commands to be querried as scope settings
setting_commands = ['TIME_DIV', 'COMM_FORMAT', 'COMM_HEADER', 'COMM_ORDER'] + \
    ['TRIG_DELAY', 'TRIG_SELECT', 'TRIG_MODE', 'TRIG_PATTERN', 'SEQUENCE'] + \
    ['C%i:COUPLING' % i for i in range(1,5)] + \
    ['C%i:VOLT_DIV' % i for i in range(1,5)] + \
    ['C%i:OFFSET' % i for i in range(1,5)] + \
    ['C%i:TRIG_COUPLING' % i for i in range(1,5)] + \
    ['C%i:TRIG_LEVEL' % i for i in range(1,5)] + \
    ['C%i:TRIG_SLOPE' % i for i in range(1,5)] + \
    ['C%i:TRACE' % i for i in range(1,5)]

# byte length of wavedesc block
wavedesclength = 346

# template of wavedesc block, where each entry in tuple is:
# (variable name, byte position from beginning of block, datatype)
wavedesc_template = ( ('descriptor_name'    , 0   , String),
                      ('template_name'      , 16  , String),
                      ('comm_type'          , 32  , Enum),
                      ('comm_order'         , 34  , Enum),
                      ('wave_descriptor'    , 36  , Long),
                      ('user_text'          , 40  , Long),
                      ('res_desc1'          , 44  , Long),
                      ('trigtime_array'     , 48  , Long),
                      ('ris_time_array'     , 52  , Long),
                      ('res_array1'         , 56  , Long),
                      ('wave_array_1'       , 60  , Long),
                      ('wave_array_2'       , 64  , Long),
                      ('res_array_2'        , 68  , Long),
                      ('res_array_3'        , 72  , Long),
                      ('instrument_name'    , 76  , String),
                      ('instrument_number'  , 92  , Long),
                      ('trace_label'        , 96  , String),
                      ('reserved1'          , 112 , Word),
                      ('reserved2'          , 114 , Word),
                      ('wave_array_count'   , 116 , Long),
                      ('pnts_per_screen'    , 120 , Long),
                      ('first_valid_pnt'    , 124 , Long),
                      ('last_valid_pnt'     , 128 , Long),
                      ('first_point'        , 132 , Long),
                      ('sparsing_factor'    , 136 , Long),
                      ('segment_index'      , 140 , Long),
                      ('subarray_count'     , 144 , Long),
                      ('sweeps_per_acq'     , 148 , Long),
                      ('points_per_pair'    , 152 , Word),
                      ('pair_offset'        , 154 , Word),
                      ('vertical_gain'      , 156 , Float),
                      ('vertical_offset'    , 160 , Float),
                      ('max_value'          , 164 , Float),
                      ('min_value'          , 168 , Float),
                      ('nominal_bits'       , 172 , Word),
                      ('nom_subarray_count' , 174 , Word),
                      ('horiz_interval'     , 176 , Float),
                      ('horiz_offset'       , 180 , Double),
                      ('pixel_offset'       , 188 , Double),
                      ('vertunit'           , 196 , UnitDefinition),
                      ('horunit'            , 244 , UnitDefinition),
                      ('horiz_uncertainty'  , 292 , Float),
                      ('trigger_time'       , 296 , TimeStamp),
                      ('acq_duration'       , 312 , Float),
                      ('record_type'        , 316 , Enum),
                      ('processing_done'    , 318 , Enum),
                      ('reserved5'          , 320 , Word),
                      ('ris_sweeps'         , 322 , Word),
                      ('timebase'           , 324 , Enum),
                      ('vert_coupling'      , 326 , Enum),
                      ('probe_att'          , 328 , Float),
                      ('fixed_vert_gain'    , 332 , Enum),
                      ('bandwidth_limit'    , 334 , Enum),
                      ('vertical_vernier'   , 336 , Float),
                      ('acq_vert_offset'    , 340 , Float),
                      ('wave_source'        , 344 , Enum) )

headerformat = '>BBBBL'

errors = { 1  : 'unrecognized command/query header',
           2  : 'illegal header path',
           3  : 'illegal number',
           4  : 'illegal number suffix',
           5  : 'unrecognized keyword',
           6  : 'string error',
           7  : 'GET embedded in another message',
           10 : 'arbitrary data block expected',
           11 : 'non-digit character in byte count field of arbitrary data block',
           12 : 'EOI detected during definite length data block transfer',
           13 : 'extra bytes detected during definite length data block transfer' }

class LeCroyScope(object):
    '''
    A class for triggering and fetching waveforms from a LeCroy oscilloscope.
    '''
    def __init__(self,  host, port=1861, timeout=5.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.settimeout(timeout)
        self._clear()
        self._send('comm_header short')
        self._check_last_command()
        self._send('comm_format DEF9,BYTE,BIN')
        self._check_last_command()


    def __del__(self):
        self.sock.close()

    def _clear(self, timeout=0.5):
        '''
        Clear any bytes in the oscilloscope's output queue by receiving
        packets until the connection blocks for more than `timeout` seconds.
        '''
        t = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        try:
            while True:
                self.sock.recv(4096)
        except socket.timeout:
            pass
        self.sock.settimeout(t)

    def _send(self, msg):
        '''
        Format and send the string `msg`.
        '''
        if not msg.endswith('\n'):
            msg += '\n'
        header = struct.pack(headerformat, 129, 1, 1, 0, len(msg))
        msg = msg.encode()
        self.sock.sendall(header + msg)

    def _recv(self):
        '''
        Return a message from the scope.
        '''
        reply = b''
        while True:
            header = b''
            while len(header) < 8:
                header += self.sock.recv(8 - len(header))
            operation, headerver, seqnum, spare, totalbytes = \
                struct.unpack(headerformat, header)
            buffer = b''
            while len(buffer) < totalbytes:
                buffer += self.sock.recv(totalbytes - len(buffer))
            reply += buffer
            if operation % 2:
                break
        return reply

    def _check_last_command(self):
        """
        Check that the last command sent was received okay; if not, raise
        an exception with details about the error.
        """
        self._send('cmr?')
        err = int(self._recv().decode().split(' ')[-1].rstrip('\n'))

        if err in errors:
            self.sock.close()
            raise Exception(errors[err])

    @property
    def settings(self):
        '''
        Captures the current settings of the scope as a dict of Command->Setting.
        '''
        settings = {}
        for command in setting_commands:
            self._send(command + '?')
            settings[command] = self._recv().strip()
            self._check_last_command()
        self._settings = settings
        return self._settings

    @settings.setter
    def settings(self, settings):
        '''
        Sends a `settings` dict of Command->Setting to the scope.
        '''
        for command, setting in settings.items():
            print('sending{:.s}'.format(command))
            self._send(setting)
            self._check_last_command()

        _ = self.settings

    @property
    def active_channels(self):
        '''
        Returns a list of the active channels on the scope.
        '''
        channels = []
        for i in range(1, 5):
            self._send('c%i:trace?' %i)
            if 'ON' in self._recv():
                channels.append(i)
        self._active_channeles = channels
        return self._active_channeles


    def trigger(self):
        '''
        Arms the oscilliscope and instructs it to wait before processing
        further commands, i.e. nonblocking.
        '''
        self._send('arm;wait')

    def _set_sequence_mode(self, nsequence):
        '''
        Sets the scope to use sequence mode for aquisition.
        '''
        if nsequence == 1:
            self._send('seq off')
        else:
            self._send('seq on,%i'%nsequence)

    def _get_wavedesc(self, channel):
        '''
        Requests the wave descriptor for `channel` from the scope. Returns it in
        dictionary format.
        '''
        if channel not in range(1, 5):
            raise Exception('channel must be in %s.' % str(range(1, 5)))

        self._send('c%s:wf? desc' % str(channel))

        msg = self._recv()
        # print(msg[1])

        # if not int(msg[1]) == channel:
        #     raise RuntimeError('waveforms out of sync or comm_header is off.')


        data = io.BytesIO(msg)
        startpos = re.search(b'WAVEDESC', data.read()).start()

        wavedesc = {}

        # check endian
        data.seek(startpos + 34)
        if struct.unpack('<'+Enum.packfmt, data.read(Enum.length)) == 0:
            endian = '>'
            wavedesc['little_endian'] = True
            np.little_endian = True
        else:
            endian = '<'
            wavedesc['little_endian'] = False
            np.little_endian = False
        data.seek(startpos)

        # build dictionary of wave description
        for name, pos, datatype in wavedesc_template:
            raw = data.read(datatype.length)
            if datatype in (String, UnitDefinition):
                wavedesc[name] = raw.rstrip(b'\x00')
            elif datatype in (TimeStamp,):
                wavedesc[name] = struct.unpack(endian+datatype.packfmt, raw)
            else:
                wavedesc[name] = struct.unpack(endian+datatype.packfmt, raw)[0]

        # determine data type
        if wavedesc['comm_type'] == 0:
            wavedesc['dtype'] = np.int8()
        elif wavedesc['comm_type'] == 1:
            wavedesc['dtype'] = np.int16()
        else:
            raise Exception('unknown comm_type.')
        return wavedesc

    @property
    def trace(self):
        '''
        Capture the raw data for `channel` from the scope and return a tuple
        containing the wave descriptor and a numpy array of the digitized
        scope readout.
        '''
        self._send('c{:d}:wf? dat1'.format(self._ch_read))
        msg = self._recv().decode('cp1252')
        # ipdb.set_trace()
        if not int(msg[1]) == self._ch_read:
            raise RuntimeError('waveforms out of sync or comm_header is off.')
        wavedesc = self._get_wavedesc(self._ch_read)
        y = np.fromstring(msg[22:], wavedesc['dtype'], wavedesc['wave_array_count'])
        x = np.linspace(0 , wavedesc['horiz_interval']*y.size, y.size )

        return pd.DataFrame({'x':x,'y': y}) , wavedesc

    @property
    def trace_select(self):
        return self._ch_read

    @trace_select.setter
    def trace_select(self, channel):
        self._ch_read = channel

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    scope = LeCroyScope('169.0.0.2')
    # plt.close('all')
    # a, b = scope.get_waveform(3)
    # f, ax = plt.subplots()
    # ax.plot(b[::10])
    # f.show()
    scope.sock.close()
