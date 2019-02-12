# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
SEGUNDA = 0
TERCA = 1
QUARTA = 2
QUINTA = 3
SEXTA = 4
SABADO = 5
DOMINGO = 6

def calc_data(data, hora, minuto):
    return datetime(data.year, data.month, data.day, hora, minuto)
# calc_data()

def calc_tempo_str(tempo):
    return "%d:%02d" % ((tempo.day - 1) * 24 + tempo.hour, tempo.minute)
# calc_tempo()

class Horas(object):
    "Classe Horas"

    def __init__(self, escalas, ignore_list, sobreaviso_list):
        self.escalas = escalas
        self.ignore_list = ignore_list
        self.sobreaviso_list = sobreaviso_list

        self.tempo_total_str = None
        self.tempo_noturno_str = None
        self.tempo_diurno_str = None
        self.tempo_diurno_especial_str = None
        self.tempo_sobreaviso_str = None
        self.tempo_reserva_str = None
        self.tempo_faixa2_str = '0:00'
    # __init__()

    def calc_saidas_chegadas(self):
        """Cálculo de chegadas e saidas"""

        segundos_diurno_especial = 0
        segundos_diurno = 0
        segundos_noturno = 0
        segundos_noturno_especial = 0
        segundos_sobreaviso = 0
        segundos_reserva = 0

        def cal_segs_voo(std, sta):
            delta = std - sta
            return delta.seconds

        for voo in self.escalas:
            chegada_18h = calc_data(voo.std, 18, 0)

            chegada_6h = calc_data(voo.std, 6, 0) + timedelta(hours=24)

            saida_18h = calc_data(voo.sta, 18, 0)

            saida_6h = calc_data(voo.sta, 6, 0)

            if voo.activity_info in self.sobreaviso_list:
                segundos_sobreaviso += cal_segs_voo(voo.std, voo.sta)

            if voo.activity_info.startswith('R') and \
                    not voo.activity_info.startswith('REU'):
                segundos_reserva += cal_segs_voo(voo.std, voo.sta)

            if voo.activity_info not in self.ignore_list and \
               not voo.activity_info.startswith('R') and \
               (not voo.duty_design or voo.duty_design == 'T'):

                if voo.sta > saida_18h and voo.std < chegada_6h:
                    segundos_noturno += cal_segs_voo(voo.std, voo.sta)
                    continue

                if voo.sta > saida_6h and voo.std < chegada_18h:
                    delta = cal_segs_voo(voo.std, voo.sta)
                    segundos_diurno += delta

                    if voo.std.weekday() == DOMINGO:
                        segundos_diurno_especial += delta
                    continue

                if voo.sta > saida_18h and voo.std > chegada_6h or \
                        voo.sta > saida_18h and voo.std > saida_6h:
                    delta = cal_segs_voo(voo.std, saida_18h)
                    segundos_noturno += delta

                    delta = chegada_18h - voo.sta
                    segundos_diurno += delta.seconds

                    if voo.std.weekday() == DOMINGO:
                        segundos_diurno_especial += delta.seconds
                    continue

                if voo.sta > saida_6h and voo.std > chegada_18h:
                    delta = voo.std - saida_18h
                    segundos_diurno += delta.seconds

                    delta = saida_18h - voo.sta
                    segundos_noturno += delta.seconds
                    if voo.std.weekday() == DOMINGO:
                        segundos_noturno_especial += delta.seconds
                    continue

                if voo.sta < saida_6h and voo.std > saida_6h:
                    delta = voo.std - saida_6h
                    segundos_diurno += delta.seconds

                    delta = saida_6h - voo.sta
                    segundos_noturno += delta.seconds
                    if voo.std.weekday() == DOMINGO:
                        segundos_noturno_especial += delta.seconds
                    continue

        segundos_total = (segundos_diurno + segundos_noturno)

        tempo_diurno = datetime(1, 1, 1) + timedelta(seconds=segundos_diurno)
        tempo_diurno_especial = datetime(1, 1, 1) + \
            timedelta(seconds=segundos_diurno_especial)

        tempo_noturno = datetime(1, 1, 1) + timedelta(seconds=segundos_noturno)
        # tempo_noturno_especial = datetime(1, 1, 1) + \
        #        timedelta(seconds=segundos_noturno)

        tempo_sobreaviso = datetime(1, 1, 1) + \
            timedelta(seconds=segundos_sobreaviso)

        tempo_reserva = datetime(1, 1, 1) + \
            timedelta(seconds=segundos_reserva)

        tempo_total = datetime(1, 1, 1) + timedelta(seconds=segundos_total)

        self.tempo_diurno_str = calc_tempo_str(tempo_diurno)

        self.tempo_noturno_str = calc_tempo_str(tempo_noturno)

        self.tempo_total_str = calc_tempo_str(tempo_total)

        self.tempo_sobreaviso_str = calc_tempo_str(tempo_sobreaviso)
        self.tempo_reserva_str = calc_tempo_str(tempo_reserva)

        self.tempo_diurno_especial_str = calc_tempo_str(
            tempo_diurno_especial)

        if ((tempo_total.day - 1) * 24 + tempo_total.hour) > 70:
            self.tempo_faixa2_str = "%d:%02d" % \
                ((tempo_total.day - 1) * 24 + tempo_total.hour - 70,
                 tempo_total.minute)

    # calc_saidas_chegadas()
