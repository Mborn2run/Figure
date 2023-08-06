#!/usr/bin/env python
# encoding: utf-8
import RPi.GPIO as GPIO
import time

class Puller:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)

    def forward(self, waiting_time):
        GPIO.output(18, True)
        GPIO.output(22, False)
        time.sleep(waiting_time)
        self.stop()
    
    def backward(self, waiting_time):
        GPIO.output(18, False)
        GPIO.output(22, True)
        time.sleep(waiting_time)
        self.stop()

    def stop(self):
        GPIO.output(18, False)
        GPIO.output(22, False)
