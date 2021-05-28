import socket
import numpy as np
import time


class NFstage(object):
    def __init__(self,**kwargs):
        address = kwargs.get('address', None)


        self.instr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.instr.settimeout(0.015)
        self.instr.connect((address,23))
        
        self.start_word = b'GO a1'
        self.stop_word = b'HAL'
        self.for_word = b'FOR a1 g'
        self.back_word = b'REV a1 g'
        self.vel_word = b'RES '
        self.end_word = b'\n'

        self.velocity = {'fine': b'FINE',
                         'coarse': b'COARSE'}

        self.instr.send(b'MON a1\n')
        self.instr.send(b'JOF\n')
        self.EmptyBuffer()

    def EmptyBuffer(self):
        dum = b''
        while True:
            try:
                dum += self.instr.recv(1)
            except:
                break
        print(dum.decode())

    def StartMotion(self,drction,veltype):
        self.instr.send(self.vel_word + 
                        self.velocity[veltype] + 
                        self.end_word)
        self.EmptyBuffer()
        # time.sleep(0.025)
        if drction == 'forward':
            print('Direction Forward')
            print('Resolution: ' + self.velocity[veltype].decode())
            print(self.for_word + self.velocity[veltype])
            self.instr.send(self.for_word + 
                            self.end_word)
            self.EmptyBuffer()
        if drction == 'backward':
            print('Direction Backward')
            print('Resolution: ' + self.velocity[veltype].decode())
            self.instr.send(self.back_word + 
                            self.end_word)
            self.EmptyBuffer()

        # self.instr.send(self.start_word + self.end_word)
        self.EmptyBuffer()

    def StopMotion(self):
        self.instr.send(self.stop_word + self.end_word)
        self.EmptyBuffer()