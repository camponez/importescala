#!/usr/bin/python
# coding=utf-8
print "Content-type: text/html\n\n"

from datetime import datetime
#from datetime import time as dtime
from datetime import timedelta
import time
import os
import dirs
import traceback
import sys
from list_aeroportos import aeroportos
from func import load_xml
from func import load_string_xml
from func import format_date
from func import strfdate

from __version__ import MINOR
from __version__ import MAJOR

VERSION = MAJOR + '.' + MINOR


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
        self.__parser(root)

    def __load_list(self):
        """
        Load lista de tipos
        """
        # Periodico
        self.periodico = ['PP1', 'PP2', 'PC1']

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
        self.simulador = ['S04', 'S05', 'S06', 'S12', 'S20']

        self.ignore_list += self.simulador




    def __parser(self, root):
        """
        Parser
        """

        for child in root:
            voo = Voo()
            d_saving = 0

            datahora = time.strptime(child[11].text, "%d/%m/%Y %H:%M:%S")
            voo.activity_date = datetime.fromtimestamp(time.mktime(datahora))

            # offset de horario de verão
            #d_saving = 1

            #ajustando horario para UTC-3
            voo.activity_date = voo.activity_date - timedelta(hours=3 + d_saving)

            voo.present_location = child[8].text

            #decolagem
            voo.sta = datetime(voo.activity_date.year,
                               voo.activity_date.month,
                               voo.activity_date.day,
                               int(child[16].text[:-3]),
                               int(child[16].text[3:]))

            #pouso
            voo.std = datetime(voo.activity_date.year,
                               voo.activity_date.month,
                               voo.activity_date.day,
                               int(child[15].text[:-3]),
                               int(child[15].text[3:]))

            # se houver mudanca de dia
            if voo.sta.time() > voo.std.time():
                voo.std = voo.std + timedelta(days=1)

            # ajuste horario de verao
            voo.sta = voo.sta - timedelta(hours=d_saving)
            voo.std = voo.std - timedelta(hours=d_saving)

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
        Criando arquivoi CSV
        """

        csv = 'Subject,Start Date,Start Time,End Date,End Time,'+\
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
                csv += 'Reserva('+voo.activity_info+'),'
                csv += format_date(voo)
                csv += 'False,,-\n'
                continue

            if voo.activity_info in self.simulador:
                csv += 'Simulador,'
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
                #Data hora inicial
                csv += strfdate(voo.activity_date) + ","
                csv += voo.checkin_time.strftime('%H:%M') + ","
                csv += strfdate(voo.activity_date) + ","
                csv += voo.checkin_time.strftime('%H:%M') + ","
                csv += 'False,"'
                if voo.origin in aeroportos:
                    csv += aeroportos[voo.origin]
                csv += '",-\n'

            csv += "Voo "+ voo.origin + '-' +voo.destination +\
                    ' ' + voo.activity_info
            if voo.duty_design:
                csv += " (E)"

            csv += ","
            csv += format_date(voo)

            csv += 'False,"'
            if voo.origin in aeroportos:
                csv += aeroportos[voo.origin]

            csv += '",Horas de voo: '
            csv += voo.horas_de_voo

            csv += '\n'

        return csv

    def get_numero_voos(self):
        """
        Número de voos
        """
        return len(self.escalas)

    def soma_horas(self):
        """
        Soma de horas
        """
        segundos = 0

        for voo in self.escalas:
            if voo.activity_info not in self.ignore_list and \
                    not voo.activity_info.startswith('R') and \
                    not voo.duty_design:
                delta = voo.std - voo.sta

                segundos += delta.seconds

        minutos = segundos / 60

        tempo = datetime(1, 1, 1) + timedelta(minutes=minutos)

        return  str(tempo.hour) + ":" + str(tempo.minute)

class Voo:
    """
    Classe que representa um voo
    """
    def __init__(self):
        self.activity_date = None
        self.present_location = None
        self.flight_no = None
        self.origin = None
        self.destination = None
        self.actype = None
        self.checkin = None
        self.checkin_time = None
        self.std = None
        self.sta = None
        self.activity_info = None
        self.duty_design = None
        self.horas_de_voo = None

if __name__ == "__main__":
    print "<html><head>"
    print "<meta http-equiv='Content-Type' content='text/html;charset=UTF-8'>"
    print "</head><body>"
    print "<table><tr><td>"
    print open('how-to.html').read()
    print "</td><td>"
    print "<div style='text-align:center'><p>Changelog</p></div>"
    print "<ul>"
    print open('changelog.html').read()
    print "</ul>"
    print "</td></tr></table>"
    print "<span>"+VERSION+"</span>"
    print '<form action="escala.py" method="post" enctype="multipart/form-data">'
    print 'Upload file: <input type="file" name="myfile" /> <br />'
    print ' <input type="submit" name="submit" value="Submit" />'
    print ' </form>'
    try:
        import uuid
        import cgi
        FORM_DATA = cgi.FieldStorage()

        TMP_ESCALA = 'tmp/' + str(uuid.uuid4().get_hex().upper()[0:6]) + '.csv'

        FILE_DATA = None
        if 'myfile' in FORM_DATA:
            FILE_DATA = FORM_DATA['myfile'].value
        else:
            if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
                XML = sys.argv[1]
            else:
                XML = 'escala.xml'
            if os.path.exists(XML):
                F = open(XML)
                FILE_DATA = F.read()

        if FILE_DATA:
            ESCALA = Escala(string_xml=FILE_DATA)

            OUTPUT = ESCALA.csv()

            F = open(TMP_ESCALA, 'w+')
            F.write(OUTPUT)
            F.close()

            print "<p>Horas de voo: "+ str(ESCALA.soma_horas()/60) + "</p>"
            if 'myfile' in FORM_DATA:
                print "<a href='" + TMP_ESCALA + "'>escala.csv</a>"
            print "<pre>" + OUTPUT + "</pre>"
    except:
        print "Unexpected error:", sys.exc_info()[1]
        print traceback.format_exc()



    print "</body></html>"

# vim:tabstop=4:expandtab:smartindent
