import time
import protocols as p
import ble_uart
# Adafruit Feather Bluefruit Sense with nRF52840
import sys

if sys.platform != 'nRF52840':
    print("Only Adafruit Feather Bluefruit Sense with nRF52840 supported")

if sys.implementation[0] != 'circuitpython' or sys.implementation[1] !=(7, 3, 2) or sys.implementation[2]!=517:
    print('warning, possible version mismatch')

import adafruit_bmp280

import board
from digitalio import DigitalInOut, Direction, Pull

import neopixel

class OnboardLEDs:
    def __init__(self):
        self.blue_led = DigitalInOut(board.BLUE_LED)
        self.blue_led.switch_to_output()
        self.blue(0)

        self.red_led = DigitalInOut(board.RED_LED)
        self.red_led.switch_to_output()
        self.red(0)

        # self.switch = DigitalInOut(board.SWITCH)
        # self.red_led.switch_to_input(pull=Pull.UP)

        # Neopixel
        self.rgbneopixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.rgbneopixel[0]=(0,0,0)

    def blue(self, value):
        assert value in [0,1]
        self.blue_led.value = value

    def red(self, value):
        assert value in [0,1]        
        self.red_led.value = value

    def rgb(self, r=0,g=0,b=0):
        self.rgbneopixel[0] = (r,g,b)

class pressure_sensor:
    def __init__(self):
        self.i2c = board.I2C()
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c) # temp & baro
        self.bmp280.sea_level_pressure = 1013.25
        self.bmp280.mode = adafruit_bmp280.MODE_NORMAL
        self.bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
        self.bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
        self.bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
        self.bmp280.overscan_temperature = adafruit_bmp280.OVERSCAN_X2
        self.prev_altitude = self.bmp280.altitude
        self.prev_time = time.monotonic()

    def get_altitude(self):
        return self.bmp280.altitude

    def get_vario(self):
        altitude_now = self.get_altitude()
        time_now = time.monotonic()
        climb = (altitude_now - self.prev_altitude) / (time_now - self.prev_time)
        self.prev_altitude = altitude_now
        self.prev_time = time_now
        
        return climb

def main():
    baro = pressure_sensor()
    leds = OnboardLEDs()
    leds.red(0)
    leds.rgb()

    ble = ble_uart.MyBLE('Flying Snake')

    print ('Waiting for BLE connection')

    while True:
        leds.rgb(r=10)
        ble.start_advertising()
        while not ble.connected():
            # blink blue LED
            leds.blue(1)
            time.sleep(0.1)
            leds.blue(0)
            time.sleep(0.1)

        # BLE connection established, stop advertising and set blue LED on
        ble.ble.stop_advertising()
        leds.blue(1)

        baro.get_vario()
        leds.rgb(g=10)
        while ble.connected():
            # blink RED led during measurement
            leds.red(1)
            climb = baro.get_vario()
            alt = baro.get_altitude()
            leds.red(0)
            nmea = p.setNmeaShortLXWP0(varioAlt=alt,climbRate=climb)
            # blink rgb LED during BLE communication (cannot be seen)
            leds.rgb(b=10, g=10)
            ble.write(nmea)
            leds.rgb(b=0, g=10)

            print(nmea[:-2])

            time.sleep(1)
        print ('BLE Disconnected')


        




