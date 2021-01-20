#! /usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
import sys

pinRed = 27
pinGreen = 22
pinBlue = 10
 
# GPIO setup.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pinRed, GPIO.OUT)
GPIO.setup(pinGreen, GPIO.OUT)
GPIO.setup(pinBlue, GPIO.OUT)

while True:
	GPIO.output(pinRed, 1)
	GPIO.output(pinGreen, 0)
	GPIO.output(pinBlue, 0)
	sleep(1)
	GPIO.output(pinRed, 0)
	GPIO.output(pinGreen, 1)
	GPIO.output(pinBlue, 0)
	sleep(1)
	GPIO.output(pinRed, 0)
	GPIO.output(pinGreen, 0)
	GPIO.output(pinBlue, 1)
	sleep(1)