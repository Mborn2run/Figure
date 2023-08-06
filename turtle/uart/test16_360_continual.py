# -*- coding:utf-8 -*-
import binascii
import serial
import time
#配置串口
ser = serial.Serial("/dev/ttyAMA0", 9600)

def UARTServo(servonum, angle):
    servonum = 64 + servonum
    date1 = int(angle/100 + 48)
    date2 = int((angle%100)/10 + 48)
    date3 = int(angle%10 + 48)
    cmd=bytearray([36,servonum,date1,date2,date3,35])
    ser.write(cmd)
    time.sleep(0.05)

UARTServo(16,85)
time.sleep(2)

UARTServo(16,90)
time.sleep(6)
UARTServo(16,170)
time.sleep(6)
UARTServo(16,85)
time.sleep(2)

UARTServo(16,43)
time.sleep(6)
UARTServo(16,85)
time.sleep(2)
