import unittest
import sys
from datetime import datetime
from datetime import time

from escala import Escala
import dirs

dirs.default_dir = dirs.TestDir()

class FrameTest(unittest.TestCase):

    def setUp(self):
        self.escala = Escala('escala.xml')

    def tearDown(self):
        pass

    def test_AttributosPrimeiroVoo(self):
        p_voo = self.escala.escalas[0]

        self.assertEqual(p_voo.activity_date,datetime(2013,3,1,11,36))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4148')
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'GYN')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(10,36))
        self.assertEqual(p_voo.std, time(13,13))
        self.assertEqual(p_voo.sta, time(11,36))
        self.assertEqual(p_voo.activity_info, 'AD4148')

    def test_AttributosSegundoVoo(self):
        p_voo = self.escala.escalas[1]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.activity_info, 'AD4148')

    def test_AttributosQuartoVoo(self):
        p_voo = self.escala.escalas[4]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.flight_no,None)
        self.assertEqual(p_voo.activity_info, 'FR')

    def test_DiaSemVoo(self):
        p_voo = self.escala.escalas[3]

    def test_NumerosVoos(self):
        self.assertEqual(self.escala.get_numero_voos(),7)

    def test_CSV(self):
        self.assertEqual(self.escala.csv(),'Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description\nCheckin,03/01/2013,10:36,03/01/2013,10:36,False,-\nFlight AD4148 VCP-GYN,03/01/2013,11:36,03/01/2013,13:13,False,-\nFlight AD4148 GYN-PMW,03/01/2013,13:55,03/01/2013,15:15,False,-\nCheckin,04/01/2013,12:28,04/01/2013,12:28,False,-\nFlight AD4049 CNF-VCP,04/01/2013,13:13,04/01/2013,14:28,False,-\nFR,04/02/2013,03:15,04/02/2013,03:15,True,-\nFR,04/03/2013,03:15,04/03/2013,03:15,True,-\nREU,04/08/2013,13:40,04/08/2013,17:00,False,-\nFlight AD4148 GYN-PMW,08/05/2013,21:15,08/05/2013,22:55,False,-\n')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
