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

    def test_AttributosVoo1(self):
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
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,3,1,11,36))

    def test_AttributosVoo2(self):
        p_voo = self.escala.escalas[1]

        self.assertEqual(p_voo.activity_date,datetime(2013,3,1,13,55))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4298')
        self.assertEqual(p_voo.origin, 'GYN')
        self.assertEqual(p_voo.destination, 'PMW')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertEqual(p_voo.sta, time(23,45))
        self.assertEqual(p_voo.std, time(01,55))
        self.assertEqual(p_voo.activity_info, 'AD4298')
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,3,2,13,55))

    def test_AttributosVoo3(self):
        p_voo = self.escala.escalas[2]

        self.assertEqual(p_voo.activity_date,datetime(2013,4,1,13,13))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4049')
        self.assertEqual(p_voo.origin, 'CNF')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, 'E90')
        self.assertEqual(p_voo.sta, time(13,13))
        self.assertEqual(p_voo.std, time(14,28))
        self.assertEqual(p_voo.activity_info, 'AD4049')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(12,28))
        self.assertEqual(p_voo.duty_design, 'P')
        self.assertEqual(p_voo.data_pouso, datetime(2013,4,1,13,13))

    def test_AttributosVoo4(self):
        p_voo = self.escala.escalas[3]

        self.assertEqual(p_voo.activity_date,datetime(2013,4,2,03,15))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(03,15))
        self.assertEqual(p_voo.std, time(03,15))
        self.assertEqual(p_voo.activity_info, 'FR')
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,4,2,03,15))

    def test_AttributosVoo5(self):
        p_voo = self.escala.escalas[4]

        self.assertEqual(p_voo.activity_date,datetime(2013,4,3,03,15))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(03,15))
        self.assertEqual(p_voo.std, time(03,15))
        self.assertEqual(p_voo.activity_info, 'FR')
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,4,3,03,15))

    def test_AttributosVoo6(self):
        p_voo = self.escala.escalas[5]

        self.assertEqual(p_voo.activity_date,datetime(2013,4,8,13,40))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(13,40))
        self.assertEqual(p_voo.std, time(17,00))
        self.assertEqual(p_voo.activity_info, 'REU')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(13,40))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,4,8,13,40))

    def test_AttributosVoo7(self):
        p_voo = self.escala.escalas[6]

        self.assertEqual(p_voo.activity_date,datetime(2013,8,5,21,35))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4035')
        self.assertEqual(p_voo.origin, 'GYN')
        self.assertEqual(p_voo.destination, 'PMW')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertEqual(p_voo.sta, time(21,15))
        self.assertEqual(p_voo.std, time(22,55))
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.activity_info, 'AD4035')
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,8,5,21,35))

    def test_AttributosVoo8(self):
        p_voo = self.escala.escalas[7]

        self.assertEqual(p_voo.activity_date,datetime(2013,9,4,8,16))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(8,16))
        self.assertEqual(p_voo.std, time(14,15))
        self.assertEqual(p_voo.activity_info, 'R08')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(8,15))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,9,4,8,16))

    def test_AttributosVoo9(self):
        p_voo = self.escala.escalas[8]

        self.assertEqual(p_voo.activity_date,datetime(2013,9,5,4,46))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(4,46))
        self.assertEqual(p_voo.std, time(8,45))
        self.assertEqual(p_voo.activity_info, 'R04')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(4,45))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,9,5,4,46))

    def test_AttributosVoo10(self):
        p_voo = self.escala.escalas[9]

        self.assertEqual(p_voo.activity_date,datetime(2013,9,8,11,00))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.activity_info, 'P11')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, time(11,00))
        self.assertEqual(p_voo.std, time(23,00))
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, time(11,00))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.data_pouso, datetime(2013,9,8,11,00))

    def test_AttributosQuartoVoo(self):
        p_voo = self.escala.escalas[4]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.flight_no,None)
        self.assertEqual(p_voo.activity_info, 'FR')

    def test_DiaSemVoo(self):
        p_voo = self.escala.escalas[3]

    def test_NumerosVoos(self):
        self.assertEqual(self.escala.get_numero_voos(),13)

    def test_CSV(self):
        check_output = '\
Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location,Description\n\
Checkin,03/01/2013,10:36,03/01/2013,10:36,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-GYN,03/01/2013,11:36,03/01/2013,13:13,False,"Aeroporto Internacional Viracopos",AD4148\n\
Voo GYN-PMW,03/01/2013,23:45,03/02/2013,01:55,False,"Aeroporto Santa Genoveva",AD4298\n\
Checkin,04/01/2013,12:28,04/01/2013,12:28,False,"Aeroporto Internacional Tancredo Neves",-\n\
Voo CNF-VCP (E),04/01/2013,13:13,04/01/2013,14:28,False,"Aeroporto Internacional Tancredo Neves",AD4049\n\
FR 03:15,04/02/2013,03:15,04/02/2013,03:15,False,,-\n\
FR 03:15,04/03/2013,03:15,04/03/2013,03:15,False,,-\n\
REU,04/08/2013,13:40,04/08/2013,17:00,False,,-\n\
Voo GYN-PMW,08/05/2013,21:15,08/05/2013,22:55,False,"Aeroporto Santa Genoveva",AD4035\n\
Reserva,09/04/2013,08:16,09/04/2013,14:15,False,,-\n\
Reserva,09/05/2013,04:46,09/05/2013,08:45,False,,-\n\
SobAviso,09/08/2013,11:00,09/08/2013,23:00,False,,-\n\
Reserva,09/09/2013,10:00,09/09/2013,14:00,False,,-\n\
SobAviso,10/09/2013,10:00,10/09/2013,14:00,False,,-\n\
Simulador,11/09/2013,10:00,11/09/2013,14:00,False,,-\n'

        self.assertEqual(self.escala.csv(), check_output)

    def test_CalculoHorasVoadas(self):
        self.assertEqual(self.escala.somaHoras(), 327)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
