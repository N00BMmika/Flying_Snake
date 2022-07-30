# Flying Snake

## About this project
Android phones have good flight computer programs like [XCTRack](https://xctrack.org/). Also low cost Android can run such program. Drawback is that in low cost phones/tablets there are no barometer at all or there is only a low accuracy barometer.

The purpose of this project is to provide high quality barometer data to (low cost) Android phone which is running flight computer application like [XCTRack](https://xctrack.org/) from relatively low cost sensor board [Adafruit Feather](https://learn.adafruit.com/adafruit-feather) using BLE connection.

Additional purpose of this project may be to make other flight computer functionality for stand alone use or for flight computer applications like [XCTRack](https://xctrack.org/).

## HW and SW setup
 The MCU board to be used is [Adafruit Feather nRF52840 Sense](https://www.adafruit.com/product/4516) since it has good barometer sensor [BMP280](https://www.adafruit.com/product/2651). Other onboard sensors gives possibility for developing more flight computer features.
[CircuitPython](https://circuitpython.org/) is used for programming the board since it is very efficient to develop applications with python and CircuitPython have very good sw libraries in place for sensor access and BLE connectivity.

### CircuitPython version
CircuitPython version used during development is 7.3.2. Copy of the Firmware and used CircuptPython libraries are stored in separate repository. This is done for avoiding possible API breaks during version changes. 

### Installation
#### CircuitPython Firmware
Latest CircuitPython could be used or alternatively the same version what was used for development:
- See Circuitpython flashing procedure from https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython#start-the-uf2-bootloader-2977081. 
The used CircuitPython firmware is in circuitpython_binaries\FW\
#### CircuitPython libraries
- Copy needed CircuitPython libraries from circuitpython_binaries\CIRCUITPY\lib to CIRCUITPY drive lib/ directory.
#### Flying Snake Application
- Copy all Python files from CIRCUITPY/ to CIRCUITPY drive

## Related projects and background of this project

There are already several similar projects made earlier. Some of those are listed here https://xctrack.org/External_Devices.html. Those are using "older" embedded programming methods (e.g. not Python language) and may also need soldering work. Since Adafruit Feather nRF52840 Sense has needed sensors already onboard and CircuitPython is supported, it looks that making low cost high accuracy variometer would be relatively easy task.

## Future plans
- improve barometer data sampling rate and noise filtering to provide faster response for altitude changes
- use accelerometer data for faster thermal detection
- use gyro and mag data for calculating thermalling circle duration
- add support for OLED display (https://www.adafruit.com/product/4650)
- add audio for variometer and other possible purposes
