import serial
import time
import random


if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()
    while True:
        time.sleep(10)
        pessoas = str(random.randint(2, 10)).encode()
        print(pessoas)
        ser.write(pessoas)
        print("Valor enviado ao serial!")