# -*- coding:utf-8 -*-
import binascii
import serial
import time

class Servo():
    def __init__(self):
        #配置串口
        self.ser = serial.Serial("/dev/ttyAMA0", 9600)
    

    def UARTServo(self, servonum, angle):
        self.servonum = 64 + servonum
        date1 = int(angle/100 + 48)
        date2 = int((angle%100)/10 + 48)
        date3 = int(angle%10 + 48)
        cmd=bytearray([36,self.servonum,date1,date2,date3,35])
        self.ser.write(cmd)
        time.sleep(0.05)

