import serial,time
import random

MYCOM = "/dev/ttyUSB0"

def getMass():
    try:
        with serial.Serial(MYCOM, 9600,timeout=2) as ser:
            ser.write('SI\r\n'.encode())
            time.sleep(.1)
            data = ser.readline()
        try:
            mass = float(data.decode().split(" g")[0].split(" ")[-1])
        except:
            mass = 0
        return mass
    except:
        # print('Failed reading')
        return 0
        # return random.randrange(0, 2500, 1)

def zero():
    try:
        with serial.Serial(MYCOM, 9600,timeout=.5) as ser:
            ser.write('T\r\n'.encode())
            time.sleep(.25)

        return " "
    except:
        print('Could not zero')
