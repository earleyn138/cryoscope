import time
import serial
import io
import csv
from datetime import datetime

def create_ser(baudrate, port, parity, bytesize, stopbits, timeout):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = port
    ser.parity=parity
    ser.bytesize=bytesize
    ser.stopbits=stopbits
    ser.timeout=timeout
    return ser

def read_pressure(ser):
    ser.write(b"?GA1\r\n")
    #sio.flush()
    pressure = ser.readline()
    time.sleep(0.334) #3 commands per second max
    return float(pressure)

def read_temp(ser):
    ser.write(b"KRDG? A\r\n")
    #sio.flush()
    temp = ser.readline()
    time.sleep(0.05) #20 commands per second max
    return float(temp)

def write_measurement(start_time, pser, tser, filename):
    now = time.time() # current date and time
    pressure = read_pressure(pser)
    temp = read_temp(tser)
    timepoint = now-start_time
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timepoint, pressure, temp])

    print("Time elapsed: {:.3f} sec, Pressure: {} Torr, Temperature: {} K".format(timepoint, pressure, temp))

# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = 'COM' #/dev/tty.usbserial-110'
# ser.parity=serial.PARITY_NONE
# ser.bytesize=serial.EIGHTBITS
# ser.stopbits=serial.STOPBITS_ONE
# ser.timeout=10
# print(ser)
# ser.open()
# print(ser.is_open)
# #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

########
filename = 'coldtest.csv'
pser = create_ser(baudrate=9600,port='COM4',parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=10)
tser = create_ser(baudrate=9600,port='COM3',parity=serial.PARITY_ODD,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,timeout=10)

with open(filename, 'w') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(["Time (s)", "Pressure (Torr)", "Temperature (K)"])

start_time = time.time()
while True:
  write_measurement(start_time, pser, tser, filename)
  time.sleep(1)


