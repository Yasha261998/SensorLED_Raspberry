# coding=utf-8
import RPi.GPIO as GPIO
from rpi_ws281x import Color, PixelStrip, ws
import time

# LED strip configuration:
LED_COUNT = 30        # количество LED пикселей.
LED_PIN = 21          # GPIO к которому подсоединена лента (должен поддерживать PWM!).
LED_FREQ_HZ = 800000  # LED частота обновления (обычно 800khz)
LED_DMA = 10          # DMA канал (попробуйте 10)
LED_BRIGHTNESS = 255  # Установить 0 для самого тёмного и 255 для самого яркого света
LED_INVERT = False    # True для иняертирования сигнала
LED_CHANNEL = 0
# LED_STRIP = ws.SK6812_STRIP_RGBW
LED_STRIP = ws.SK6812W_STRIP

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN) #PIN, к которому подсоединен сенсор
GPIO.setup(21, GPIO.OUT) #PIN, к которому присоединен светодиод

# функция для отображения определенного цвета на ленте с задержкой.
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


# Main program logic follows:
if __name__ == '__main__':
    # Создание объекта с задаными параметрами конфигурации LED ленты.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()  # Инициализация библиотеки.
    start_time = time.time()

    while True:
        i = GPIO.input(11)
        if i == 0: #Если сенсор не срабатывает (сигнал LOW)
            if time.time() - start_time > 120:
                colorWipe(strip, Color(0, 0, 0, 0), 0)  # выключить
            print("NO motion", i) #В терминале написать что движение НЕ обнаружено
            time.sleep(0.7) #время задержки перед повторной проверкой сигнала
        elif i == 1: #Если сенсор срабатывает (сигнал HIGH)
            start_time = time.time()
            print("Motion DETECTED", i) #В терминале написать что движение обнаружено
            colorWipe(strip, Color(0, 0, 0, 255), 0)  # Белый
            time.sleep(0.7) # время задержки перед повторной проверкой сигна