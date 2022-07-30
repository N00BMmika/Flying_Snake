"""
  /*
   *  $LXWP0,N,,119.9,0.16,,,,,,259,,*64
   *  0 logger stored (Y/N)
   *  1 n.u.
   *  2 baroaltitude (m)
   *  3 vario (m/s)
   *  4-8 n.u.
   *  9 course (0..360)
   * 10 n.u
   * 11 n.u.
   */

/*
   * $XCTRC,year,month,day,hour,minute,second,centisecond,latitude,longitude,
   *  altitude,speedoverground,course,climbrate,res,res,res,rawpressure,
   *  batteryindication*checksum
   * $XCTRC,2015,8,11,10,56,23,80,48.62825,8.104885,129.4,0.01,322.76,-0.05,,,,997.79,77*66
   */

"""

# https://github.com/FreeVario/FreeVarioF1/blob/master/Src/FreeVario/FreeVarioLib/nmea.c#L53
  

"""
https://downloads.lxnavigation.com/downloads/manuals/LX_CP_R5.pdf
Parameter Data type Description
<is_logger_running> char 'Y'=yes, 'N'=no
<tas> float True airspeed in km/h
<altitude> float True altitude in meters
<varioN> float 6 measurements of vario in last second in m/s
<heading> uint16_t True heading in degrees. Blank if compass not connected.
<wind_direction> string Wind direction in degrees. Blank if wind speed is 0.0.
<wind_speed> string Wind speed in km/h. Blank if wind speed is 0.0
"""

def setNmeaShortLXWP0(varioAlt: float, climbRate: float):
    """
    // short version, for high speed updates. only v1[0] given
    // $LXWP0,logger_stored, airspeed, airaltitude,
    //   v1[0],v1[1],v1[2],v1[3],v1[4],v1[5], hdg, windspeed*CS<CR><LF>
    //
    // 0 loger_stored : [Y|N] (not used in LX1600)
    // 1 IAS [km/h] ----> Condor uses TAS!
    // 2 baroaltitude [m]
    // 3-8 vario values [m/s] (last 6 measurements in last second)
    // 9 heading of plane (not used in LX1600)
    // 10 windcourse [deg] (not used in LX1600)
    // 11 windspeed [km/h] (not used in LX1600)
    //
    // e.g.:
    // $LXWP0,Y,222.3,1665.5,1.71,,,,,,239,174,10.1    
    """
    nmea = "$LXWP0,N,,%.2f,%.2f,,,,,,,,,*" % (varioAlt, climbRate)
    CRC = _getCRC(nmea)
    nmea = nmea + CRC + '\r\n'
    return nmea

def setNmeaLK8EX1(
    rawPressure:int=999999,
    varioAlt:int=99999,
    climbRate:int=9999,
    temperature:int=99,
    pbat:int=999):
    """
    Field 0, raw pressure in hPascal:
        hPA*100 (example for 1013.25 becomes  101325) 
        no padding (987.25 becomes 98725, NOT 098725)
        If no pressure available, send 999999 (6 times 9)
        If pressure is available, field 1 altitude will be ignored

    Field 1, altitude in meters, relative to QNH 1013.25
        If raw pressure is available, this value will be IGNORED (you can set it to 99999
        but not really needed)!
        (if you want to use this value, set raw pressure to 999999)
        This value is relative to sea level (QNE). We are assuming that
        currently at 0m altitude pressure is standard 1013.25.
        If you cannot send raw altitude, then send what you have but then
        you must NOT adjust it from Basic Setting in LK.
        Altitude can be negative
        If altitude not available, and Pressure not available, set Altitude
        to 99999  (5 times 9)
        LK will say "Baro altitude available" if one of fields 0 and 1 is available.

    Field 2, vario in cm/s
        If vario not available, send 9999  (4 times 9)
        Value can also be negative

    Field 3, temperature in C , can be also negative
        If not available, send 99

    Field 4, battery voltage or charge percentage
        Cannot be negative
        If not available, send 999 (3 times 9)
        Voltage is sent as float value like: 0.1 1.4 2.3  11.2 
        To send percentage, add 1000. Example 0% = 1000
        14% = 1014 .  Do not send float values for percentages.
        Percentage should be 0 to 100, with no decimals, added by 1000!

        https://github.com/LK8000/LK8000/blob/master/Docs/LK8EX1.txt
    """
    assert rawPressure != 999999 and varioAlt == 99999 or rawPressure == 999999 and varioAlt != 99999
    nmea = "$LK8EX1,%d,%d,%d,%d,%.1f*" % (rawPressure, varioAlt, climbRate, temperature, pbat)
    CRC = _getCRC(nmea)
    nmea = nmea + CRC + '\r\n'
    return nmea

# https://github.com/IvkoPivko/MiniVario-Arduino/blob/master/Latest%20version/V_18_Filter11.ino#L457
def setNmeaBFV(pressure, climbRate, temperature=10, battery=100):
    """ 
        pressure Pa
        climbRate cm/s
        temperature C
        battery %
    """
    nmea = "$BFV,%d,%d,%d,%d,*" % \
        (pressure, climbRate*100,temperature, battery)
    CRC = _getCRC(nmea)
    nmea = nmea + CRC + '\r\n'
    return nmea

def _getCRC(nmea):
    XOR = 0
    assert nmea[0] == '$'
    assert nmea[-1] == '*'
    for t in nmea[1:-1]:
        XOR ^= ord(t)

    return '%x' % XOR

