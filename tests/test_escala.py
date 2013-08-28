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
        self.assertEqual(p_voo.activity_info, 'AD4298')

    def test_AttributosQuartoVoo(self):
        p_voo = self.escala.escalas[4]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.flight_no,None)
        self.assertEqual(p_voo.activity_info, 'FR')

    def test_DiaSemVoo(self):
        p_voo = self.escala.escalas[3]

    def test_NumerosVoos(self):
        self.assertEqual(self.escala.get_numero_voos(),10)

    def test_CSV(self):
        check_output = '\
Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location,Description\n\
Checkin,03/01/2013,10:36,03/01/2013,10:36,False,,-\n\
Flight AD4148 VCP-GYN,03/01/2013,11:36,03/01/2013,13:13,False,"Aeroporto Internacional Viracopos",-\n\
Flight AD4298 GYN-PMW,03/01/2013,23:45,03/02/2013,01:55,False,"Aeroporto Santa Genoveva",-\n\
Checkin,04/01/2013,12:28,04/01/2013,12:28,False,,-\n\
Flight AD4049 CNF-VCP (E),04/01/2013,13:13,04/01/2013,14:28,False,"Aeroporto Internacional Tancredo Neves",-\n\
FR 03:15,04/02/2013,03:15,04/02/2013,03:15,False,,-\n\
FR 03:15,04/03/2013,03:15,04/03/2013,03:15,False,,-\n\
REU,04/08/2013,13:40,04/08/2013,17:00,False,,-\n\
Flight AD4035 GYN-PMW,08/05/2013,21:15,08/05/2013,22:55,False,"Aeroporto Santa Genoveva",-\n\
Reserva,09/04/2013,08:16,09/04/2013,14:15,False,,-\n\
Reserva,09/05/2013,04:46,09/05/2013,08:45,False,,-\n\
SobAviso,09/08/2013,11:00,09/08/2013,23:00,False,,-\n'

        self.assertEqual(self.escala.csv(), check_output)

    def test_CalculoHorasVoadas(self):
        self.assertEqual(self.escala.somaHoras(), 327)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
