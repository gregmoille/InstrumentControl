"""
library for fetching data from the Yokogawa OSA AQ6370C
"""
import socket
import time
import numpy as np

def OpenTCPsocket(TCP_IP, TCP_PORT, BUFFER_SIZE):
    print(TCP_IP, TCP_PORT, BUFFER_SIZE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((TCP_IP, TCP_PORT))
    except:
        print('failed opening the socket', s.error)
    # buf = s.recv(BUFFER_SIZE)

    print('Opened Socket')
    return s

def CloseTCPSocket(s):
    # time.sleep(2)
    s.close()
    print('Closed Socket')

def Read_OSA(s, BUFFER_SIZE):
    data = s.recv(BUFFER_SIZE)
    return data.decode('ascii')

def EmptyBuffer(s):
    ReadBuffer = b''
    s.send(b' \n') 
    while not ReadBuffer == b'\n':
        try:
            ReadBuffer = s.recv(1)
        except:
            break

def Write_OSA(s, MESSAGE):
    N = s.send(MESSAGE.encode())
    # readout = ''
    # ReadBuffer = s.recvfrom(BUFFER_SIZE)[0]
    # return ReadBuffer.decode('ascii').strip()


def QuerryData(s, MESSAGE, BUFFER_SIZE):
    N = s.send(MESSAGE.encode())
    readout = ''
    ReadBuffer = b' '
    KeepDoing = True
    while not ReadBuffer.decode()[-1] == '\n' :
        ReadBuffer = s.recvfrom(BUFFER_SIZE)[0]
        readout = readout + ReadBuffer.decode()
    return readout


if '__main__' == __name__: # execute only if run as a script
    TCP_IP_yokogawa = '169.254.122.3'
    TCP_PORT = 10001
    BUFFER_SIZE = 256
    OpeningYokogawa_str = 'open "anonymous"\n'
    
    s = OpenTCPsocket(TCP_IP_yokogawa, TCP_PORT, BUFFER_SIZE)
 
    buf = QuerryData(s, OpeningYokogawa_str , BUFFER_SIZE) #LOGIN step1
    print(buf)
    buf = QuerryData(s, " " + "\n" , BUFFER_SIZE) #LOGIN step2
    EmptyBuffer(s)
    # s.settimeout(100)

    print(buf)
    # print(buf) # shall be stg like "ready" when fine
    s.send(":SENS:WAV:CENT 1070nm\n".encode())
    Write_OSA(s, ":SENSe:SWEep:SPEed 1"  + "\n") #LOGIN step2
    N = QuerryData(s, ":SENSe:WAVelength:SPAN?" + "\n", BUFFER_SIZE)
    print(N)
    Write_OSA(s, ":SENSe:WAVelength:SPAN 200nm" + "\n")
    Write_OSA(s, ":INITiate:SMODe 1\n")
    Write_OSA(s, ":INITiate" + "\n")
    N = QuerryData(s, ":STATus:OPERation:CONDition?" + "\n", BUFFER_SIZE)
    print(N)
    # Write_OSA(s,":INITiate\n")

    t = time.time()
    # X = QuerryData(s, ":TRACe:X? TRA"  + "\n" , int(N)*100000) #LOGIN step2
    # Y = QuerryData(s, ":TRACe:Y? TRA"  + "\n" , int(N)*100000) #LOGIN step2
    # # time.sleep(0.25)
    # X = np.array([float(xx) for xx in X.split(',')])
    # # Y = Write_OSA(s, ":TRACe:Y? TRA"  + "\n" , int(N)*17) #LOGIN step2
    # # time.sleep(0.25)
    # Y = np.array([float(xx) for xx in Y.split(',')])
    # # 
    # Y = np.array([float(xx) for xx in Y.split(',')])
    print('Elapsed Time: ' + "{:.2f}".format(time.time() - t) + ' seconds') 
    CloseTCPSocket(s)
