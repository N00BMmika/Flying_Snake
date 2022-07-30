import time
import protocols as p
import ble_uart


def main():
    ble = ble_uart.MyBLE('mikavario')
    while not ble.connected():
        time.sleep(0.1)

    altl=[1,1,2,2,3,3,4,4,3,3,2,2,1,1,0,0,-1,-1,-2,-2,0,0]
    alt=0
    climb=2
    input_data = ble.read()
    if input_data:
        print('R', input_data)
    for t in range (100):
        for climb in altl:
            alt=1000
            nmea = p.setNmeaShortLXWP0(varioAlt=alt,climbRate=climb) # toimii
            #nmea = p.setNmeaLK8EX1(varioAlt=alt, climbRate=climb) # ei toimi
            #nmea = p.setNmeaBFV(pressure=1000+alt,climbRate=climb) # ei toimi
            alt+=(climb)
            print ('W',nmea)
            ble.write(nmea)
            time.sleep(1)

    print ('done')

