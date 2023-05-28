import serial
import time
import matplotlib.pyplot as plt

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

data = []
while True:
    line = ser.readline()   # read a byte string
    print(line)


ser.close()
