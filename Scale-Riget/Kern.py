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
            if "kg" in data.decode():
                mass = float(data.decode().split(" kg")[0].split(" ")[-1])*1000
            else:
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

''' Potentiel løsning til at vægten står og hopper
import serial
import time

MYCOM = "/dev/ttyUSB0"

def getMass():
    readings = []

    try:
        with serial.Serial(MYCOM, 9600, timeout=2) as ser:
            for _ in range(10):
                ser.write(b"SI\r\n")
                time.sleep(0.2)

                data = ser.readline().decode(errors="ignore").strip()

                try:
                    if "kg" in data:
                        mass = float(data.split(" kg")[0].split()[-1]) * 1000
                    elif "g" in data:
                        mass = float(data.split(" g")[0].split()[-1])
                    else:
                        continue

                    readings.append(mass)

                except:
                    continue

        if len(readings) >= 5:
            readings.sort()

            # Fjern laveste og højeste måling
            middle = readings[1:-1]

            # Gennemsnit uden decimaler
            return int(round(sum(middle) / len(middle)))

        return 0

    except:
        return 0'''