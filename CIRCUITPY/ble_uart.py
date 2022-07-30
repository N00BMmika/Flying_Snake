
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

class MyBLE:
    def __init__(self, name="myble"):
        self.ble = BLERadio()
        self.ble.name = name
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)

    def start_advertising(self):
        self.ble.start_advertising(self.advertisement)

    def connected(self) -> bool:
        # todo ble.stop_advertising() after connected
        return self.ble.connected

    def write(self, data):
        if self.ble.connected:
            self.uart.write(data)

    def read(self):
        if self.uart.in_waiting > 0:
            return self.uart.read()
        return None


    

    
