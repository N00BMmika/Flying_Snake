import unittest
import sys
sys.path.append('../CIRCUITPY')
import protocols

class TestNMEA(unittest.TestCase):
    def testLXWP0(self):
        result = protocols.setNmeaShortLXWP0(
            varioAlt = 1.00, 
            climbRate = 1.00)
        #print(result)
        self.assertEqual(result, '$LXWP0,N,,1.00,1.00,,,,,,,,,*41\r\n')

    def testLK8EX1(self):
        result = protocols.setNmeaLK8EX1(
            varioAlt=0,
            climbRate=1
            )
        #print(result)
        self.assertCountEqual(result, '$LK8EX1,999999,0,1,99,999.0*19\r\n')

    def testBFV(self):
        result = protocols.setNmeaBFV(
            pressure=1000,
            climbRate=2,
            temperature=20,
            battery=100
        )
        #print (result)
        self.assertEqual(result, '$BFV,1000,200,20,100,*7e\r\n')
if __name__ == '__main__':
    unittest.main()