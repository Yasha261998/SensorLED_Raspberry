#!/usr/bin/env python
# coding=utf-8

import sys
import time
import RPi.GPIO as GPIO
from neopixel import *
import subprocess

GPIO.setmode(GPIO.BCM)
SHUTOFF_DELAY = 120     # vremya zaderzhki v secundah ot viklyucheniya
PIR_PIN = 11            # Pin k kotoromu pisoedinen sensor
LED_COUNT = 24          # Количество светодиодов в ленте
LED_PIN = 21            # GPIO пин, к которому вы подсоединяете светодиодную ленту
LED_FREQ_HZ = 800000    # LED частота обновления (обычно 800khz)
LED_DMA = 10            # DMA канал
LED_BRIGHTNESS = 255    # Установить 0 для самого тёмного 255
LED_INVERT = False      # True для иняертирования сигнала
LED_CHANNEL = 0         # Set to '1' for GPIOs 13, 19, 41, 45 or 53


def main():
    GPIO.setup(PIR_PIN, GPIO.IN)
    turned_off = False

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
    strip.begin()
    colors = Color(0, 0, 0)

    print('Run')

    last_motion_time = time.time()

    while True:
        if GPIO.input(PIR_PIN):
            last_motion_time = time.time()
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                colors = turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                colors = turn_off()
        time.sleep(.1)
        colorWipe(strip, colors, wait_ms=100)  # Display color


def turn_on():                # chto delat kogda dvizhenie obnaruzheno
    print "Motion DETECTED"
    return Color(77, 77, 255)


def turn_off():               # chto delat kogda dvizheniya net
    print "NO motion"
    return Color(0, 0, 0)


def colorWipe(strip, color, wait_ms=50):  # отображение цвета по одному светодиоду за раз
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    colorWipe(strip, Color(0, 0, 0), 10)
