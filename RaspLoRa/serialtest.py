import serial
import time
import random


if __name__ == '__main__':
    
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.flush()
    while True:
        line = ser.read_until('\n').decode('utf-8').rstrip()
        print(line)
        if len(line.split('$')) > 2:
            test = line.split('$')
            print(test[1])
        time.sleep(1)