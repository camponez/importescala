# -*- coding: utf-8 -*-
from datetime import timedelta
from datetime import datetime
import time
import dirs

from lib.func import load_xml
from lib.func import load_string_xml
from lib.func import format_date
from lib.func import format_date_ics
from lib.func import strfdate
from lib.voo import Voo
from lib.horas import Horas
from list_aeroportos import aeroportos

class Escala(object):
    """
    Classe escala
    """

    def __init__(self, arquivo_xml=None, string_xml=None):

        self.escalas = []
        self.ignore_list = []
        self.periodico = None
        self.sobreaviso = None
        self.folgas = None
        self.simulador = None

        self.__load_list()

        self.data_dir = dirs.get_default_dir()

        if arquivo_xml:
            arquivo_xml = self.data_dir.get_data_file(arquivo_xml)

        if arquivo_xml:
            root = load_xml(arquivo_xml)
        else:
            root = load_string_xml(string_xml)

        self.__parser(root, 3)

    def __load_list(self):
        """
        Load lista de tipos
        """
        # Periodico
        self.periodico = ['PP1', 'PP2', 'PC1', 'GCI']

        self.ignore_list += self.periodico

        # Sobreaviso
        self.sobreaviso = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06',
                           'P07', 'P08', 'P09', 'P10', 'P11', 'P12',
                           'P', 'PLT']

        self.ignore_list += self.sobreaviso

        # Folgas
        self.folgas = ['F', 'FA', 'FR', 'FP', 'DMI', 'REU', 'FER']

        self.ignore_list += self.folgas

        # Simulador
        self.simulador = ['S04', 'S05', 'S06', 'S12', 'S20', 'T30',
                          'SBO', 'H30', 'V30']

        self.ignore_list += self.simulador

    def __parser(self, root, timezone):
        """
        Parser
        """

        for child in root:
            voo = Voo()
            d_saving = 0

            datahora = time.strptime(child[11].text, "%d/%m/%Y %H:%M:%S")
            voo.activity_date = datetime.fromtimestamp(time.mktime(datahora))

            # ajustando horario para UTC-3
            voo.activity_date = voo.activity_date - \
                timedelta(hours=timezone + d_saving)

            voo.present_location = child[8].text

            # decolagem
            voo.sta = datetime(voo.activity_date.year,
                               voo.activity_date.month,
                               voo.activity_date.day,
                               int(child[16].text[:-3]),
                               int(child[16].text[3:]))

            # pouso
            voo.std = datetime(voo.activity_date.year,
                               voo.activity_date.month,
                               voo.activity_date.day,
                               int(child[15].text[:-3]),
                               int(child[15].text[3:]))

            # se houver mudanca de dia
            if voo.sta.time() > voo.std.time():
                voo.std = voo.std + timedelta(days=1)

            voo.horas_de_voo = str(voo.std - voo.sta)[:-3]

            voo.actype = child[17].text
            voo.flight_no = child[18].text
            voo.origin = child[19].text
            voo.destination = child[20].text
            voo.duty_design = child[21].text if child[21].text is not None else False
            voo.activity_info = child[22].text

            if child[9].text is not None:
                voo.checkin = True
                voo.checkin_time = datetime(voo.activity_date.year,
                                            voo.activity_date.month,
                                            voo.activity_date.day,
                                            int(child[9].text[:-3]),
                                            int(child[9].text[3:]))
            else:
                voo.checkin = False
                voo.checkin_time = None

            self.escalas.append(voo)

    def csv(self):
        """
        Criando arquivo CSV
        """

        csv = 'Subject,Start Date,Start Time,End Date,End Time,' +\
            'All Day Event,Location,Description\n'

        for voo in self.escalas:
            if voo.activity_info in self.folgas:
                csv += voo.activity_info + ','
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.activity_info in self.periodico:
                csv += 'Periódico,'
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.activity_info.startswith('R'):
                csv += 'Reserva(' + voo.activity_info + '),'
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.activity_info in self.simulador:
                csv += 'Simulador (' + voo.activity_info + '),'
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.activity_info in self.sobreaviso:
                csv += 'SobreAviso,'
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.checkin:
                csv += 'CheckIn,'
                # Data hora inicial
                csv += strfdate(voo.activity_date) + ","
                csv += voo.checkin_time.strftime('%H:%M') + ","
                csv += strfdate(voo.activity_date) + ","
                csv += voo.checkin_time.strftime('%H:%M') + ","
                csv += 'False,"'
                if voo.origin in aeroportos:
                    csv += aeroportos[voo.origin]
                csv += '",-\n'

            csv += "Voo " + voo.origin + '-' + voo.destination +\
                ' ' + voo.activity_info
            if voo.duty_design:
                csv += " (" + voo.duty_design + ")"

            csv += ","
            csv += format_date(voo)

            csv += 'False,"'
            if voo.origin in aeroportos:
                csv += aeroportos[voo.origin]

            csv += '",Horas de voo: '
            csv += voo.horas_de_voo

            csv += '\n'

        return csv

    def ics(self):
        """
        Criando arquivo ICS
        """

        def end_event(voo):
            ics = 'DESCRIPTION:-\n'
            ics += format_date_ics(voo)
            ics += "END:VEVENT\n"
            return ics

        ics = "BEGIN:VCALENDAR\n"
        ics += "VERSION:2.0\n"
        ics += "CALSCALE:GREGORIAN\n"
        ics += "PRODID:-//Escala Azul//EN\n"
        ics += "X-WR-TIMEZONE:America/Sao_Paulo\n"

        for voo in self.escalas:
            ics += "BEGIN:VEVENT\n"
            ics += "UID:123\n"

            if voo.activity_info in self.folgas:
                ics += "SUMMARY:" + voo.activity_info + '\n'
                ics += end_event(voo)
                continue

            if voo.activity_info in self.periodico:
                ics += 'SUMMARY: Periódico\n'
                ics += end_event(voo)
                continue

            if voo.activity_info.startswith('R'):
                ics += 'SUMMARY:Reserva(' + voo.activity_info + ')\n'
                ics += end_event(voo)
                continue

            if voo.activity_info in self.simulador:
                ics += 'SUMMARY:Simulador (' + voo.activity_info + ')\n'
                ics += end_event(voo)
                continue

            if voo.activity_info in self.sobreaviso:
                ics += 'SUMMARY:SobreAviso\n'
                ics += end_event(voo)
                continue

            if voo.checkin:
                ics += 'SUMMARY:CheckIn\n'
                ics += 'DESCRIPTION:-\n'
                ics += format_date_ics(voo, True)
                ics += 'LOCATION:'
                if voo.origin in aeroportos:
                    ics += aeroportos[voo.origin] + '\n'
                ics += 'END:VEVENT\n'
                ics += 'BEGIN:VEVENT\n'
                ics += 'UID:123\n'

            ics += "SUMMARY:Voo " + voo.origin + '-' + voo.destination +\
                ' ' + voo.activity_info
            if voo.duty_design:
                ics += " (E)"
            ics += '\n'

            ics += 'DESCRIPTION:Horas de voo: '
            ics += voo.horas_de_voo + '\n'
            ics += format_date_ics(voo)

            ics += 'LOCATION:'
            if voo.origin in aeroportos:
                ics += aeroportos[voo.origin] + '\n'

            ics += 'END:VEVENT\n'

        ics += "END:VCALENDAR"

        return ics

    def get_numero_voos(self):
        """
        Número de voos
        """
        return len(self.escalas)

    def soma_horas(self):
        """
        Soma de horas
        """

        horas = Horas(self.escalas, self.ignore_list, self.sobreaviso)

        horas.calc_saidas_chegadas()

        return {
            'h_diurno': horas.tempo_diurno_str,
            'h_noturno': horas.tempo_noturno_str,
            'h_total_voo': horas.tempo_total_str,
            'h_faixa2': horas.tempo_faixa2_str,
            'h_sobreaviso': horas.tempo_sobreaviso_str,
            'h_reserva': horas.tempo_reserva_str
        }
