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
        self.assertEqual(p_voo.checkin_time, datetime(2013,3,1,10,36))
        self.assertEqual(p_voo.std, datetime(2013,3,1,13,13))
        self.assertEqual(p_voo.sta, datetime(2013,3,1,11,36))
        self.assertEqual(p_voo.activity_info, 'AD4148')
        self.assertFalse(p_voo.duty_design)

    def test_AttributosVoo17(self):
        p_voo = self.escala.escalas[17]

        self.assertEqual(p_voo.activity_date,datetime(2013,10,28,03,00))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.activity_info, 'P04')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, datetime(2013,10,28,03,00))
        self.assertEqual(p_voo.std, datetime(2013,10,28,15,00))
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertFalse(p_voo.duty_design)

    def test_AttributosVoo18(self):
        p_voo = self.escala.escalas[18]

        self.assertEqual(p_voo.activity_date,datetime(2013,10,29,04,58))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4050')
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'FLN')
        self.assertEqual(p_voo.activity_info, 'AD4050')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertEqual(p_voo.sta, datetime(2013,10,29,04,58))
        self.assertEqual(p_voo.std, datetime(2013,10,29,06,15))
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, datetime(2013,10,29,5,8))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.horas_de_voo, '1:17')

    def test_AttributosQuartoVoo(self):
        p_voo = self.escala.escalas[4]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.flight_no,None)
        self.assertEqual(p_voo.activity_info, 'FR')

    def test_NumerosVoos(self):
        self.assertEqual(self.escala.get_numero_voos(),19)

    def test_CSV(self):
        check_output = '\
Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location,Description\n\
CheckIn,03/01/2013,10:36,03/01/2013,10:36,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-GYN AD4148,03/01/2013,11:36,03/01/2013,13:13,False,"Aeroporto Internacional Viracopos",Horas de voo: 1:37\n\
Voo GYN-PMW AD4298,03/01/2013,23:45,03/02/2013,01:55,False,"Aeroporto Santa Genoveva",Horas de voo: 2:10\n\
CheckIn,04/01/2013,12:28,04/01/2013,12:28,False,"Aeroporto Internacional Tancredo Neves",-\n\
Voo CNF-VCP AD4049 (E),04/01/2013,13:13,04/01/2013,14:28,False,"Aeroporto Internacional Tancredo Neves",Horas de voo: 1:15\n\
FR,04/02/2013,03:15,04/02/2013,03:15,False,,-\n\
FR,04/03/2013,03:15,04/03/2013,03:15,False,,-\n\
REU,04/08/2013,13:40,04/08/2013,17:00,False,,-\n\
Voo GYN-PMW AD4035,08/05/2013,21:15,08/05/2013,22:55,False,"Aeroporto Santa Genoveva",Horas de voo: 1:40\n\
Reserva(R08),09/04/2013,08:16,09/04/2013,14:15,False,,-\n\
Reserva(R04),09/05/2013,04:46,09/05/2013,08:45,False,,-\n\
SobreAviso,09/08/2013,11:00,09/08/2013,23:00,False,,-\n\
Reserva(RHC),09/09/2013,10:00,09/09/2013,14:00,False,,-\n\
SobreAviso,10/09/2013,10:00,10/09/2013,14:00,False,,-\n\
Simulador,11/09/2013,10:00,11/09/2013,14:00,False,,-\n\
Reserva(R0),12/09/2013,05:00,12/09/2013,12:00,False,,-\n\
Reserva(R07),10/26/2013,06:15,10/26/2013,09:30,False,,-\n\
FP,10/06/2013,06:50,10/06/2013,06:50,False,,-\n\
Reserva(R12),10/25/2013,11:00,10/25/2013,16:00,False,,-\n\
SobreAviso,10/28/2013,03:00,10/28/2013,15:00,False,,-\n\
CheckIn,10/29/2013,05:08,10/29/2013,05:08,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-FLN AD4050,10/29/2013,04:58,10/29/2013,06:15,False,"Aeroporto Internacional Viracopos",Horas de voo: 1:17\n'

        self.assertEqual(self.escala.csv(), check_output)

    def test_CalculoHorasVoadas(self):
        self.assertEqual(self.escala.somaHoras(), 404)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
