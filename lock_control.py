#!/usr/bin/env python
# coding: utf-8

import sys
import time
import math
import RPi.GPIO as GPIO

import dothat.lcd as lcd
import dothat.backlight as backlight

if len(sys.argv) == 1:
    sys.exit(0)


lcd.clear()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

r = GPIO.PWM(18, 50)

r.start(0)

if sys.argv[1] == "authorized":
    lcd.write("Bienvenue " + sys.argv[2])
    backlight.rgb(0, 255, 0)
    r.ChangeDutyCycle(5)

if sys.argv[1] == "waiting":
    backlight.rgb(255, 255, 0)

if sys.argv[1] == "close":
    backlight.rgb(255, 255, 255)
    r.ChangeDutyCycle(10)

if sys.argv[1] == "unauthorized":
    backlight.rgb(255, 0, 0)
    lcd.write("Accès non autorisé.")

r.stop()
backlight.graph_off()
backlight.off()
lcd.clear()
GPIO.cleanup()
