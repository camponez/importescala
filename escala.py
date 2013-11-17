#!/usr/bin/python
# coding=utf-8
print "Content-type: text/html\n\n"

import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import time as dtime
from datetime import timedelta
import time
import os
import dirs
import traceback
import sys
from list_aeroportos import aeroportos

DST_INICIO = datetime(2013,10,20)
DST_FIM = datetime(2014,2,16)
VERSION = '1.12'


class Escala:
    def __init__(self, arquivo_xml=None, string_xml=None):

        self.escalas = []
        self.data_dir = dirs.get_default_dir()
        if arquivo_xml:
            arquivo_xml = self.data_dir.get_data_file(arquivo_xml)

        if arquivo_xml:
            root = self.__load_xml(arquivo_xml)
        else:
            root = self.__load_string_xml(string_xml)
        self.__parser(root)

    def __load_xml(self, arquivo_xml):
        if not os.path.exists(arquivo_xml):
           print 'Oh dear.'
           raise

        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        return root

    def __load_string_xml(self, string_xml):
	root = ET.fromstring(string_xml)

	return root

    def __parser(self, root):

        for child in root:
            voo = Voo()
            d_saving = 0

            datahora =  time.strptime(child[11].text, "%d/%m/%Y %H:%M:%S")
            voo.activity_date = datetime.fromtimestamp(time.mktime(datahora))

            # offset de horario de verão
            #if voo.activity_date > DST_INICIO and voo.activity_date < DST_FIM:
            #    d_saving = -1

            #ajustando horario para UTC-3
            voo.activity_date = voo.activity_date - timedelta(hours=3 + d_saving)

            voo.present_location = child[8].text

            #decolagem
            voo.sta = datetime(voo.activity_date.year, voo.activity_date.month,
                    voo.activity_date.day,
                    int(child[16].text[:-3]), int(child[16].text[3:]))

            #pouso
            voo.std = datetime(voo.activity_date.year, voo.activity_date.month,
                    voo.activity_date.day,
                    int(child[15].text[:-3]), int(child[15].text[3:]))

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
                voo.checkin_time = datetime(voo.activity_date.year, voo.activity_date.month,
                    voo.activity_date.day,
                    int(child[9].text[:-3]), int(child[9].text[3:]))
            else:
                voo.checkin = False
                voo.checkin_time = None

            self.escalas.append(voo)

    def csv(self):
        csv = 'Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location,Description\n'

        for voo in self.escalas:
            if voo.activity_info == 'FP':
                csv += 'FP,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv +=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info == 'FR':
                csv += 'FR,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info == 'F':
                csv += 'F,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info == 'REU':
                csv += 'REU,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info.startswith('R') or\
                    voo.activity_info == 'RHC':
                csv += 'Reserva('+voo.activity_info+'),'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info in ['S04', 'S12', 'S20']:
                csv += 'Simulador,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.activity_info in \
                    ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08',
                            'P09', 'P10', 'P11', 'P12'] or \
                    voo.activity_info == 'PLT':
                csv += 'SobreAviso,'
                csv += voo.sta.strftime('%m/%d/%Y')+","
                csv += voo.sta.strftime('%H:%M')+","
                csv+=voo.std.strftime('%m/%d/%Y')+","
                csv += voo.std.strftime('%H:%M')+","
                csv+='False,,-\n'
                continue

            if voo.checkin:
                csv += 'CheckIn,'
                #Data hora inicial
                csv += voo.activity_date.strftime('%m/%d/%Y')+","
                csv += voo.checkin_time.strftime('%H:%M')+","
                csv += voo.activity_date.strftime('%m/%d/%Y')+","
                csv += voo.checkin_time.strftime('%H:%M')+","
                csv+='False,"'
                if voo.origin in aeroportos:
                    csv+=aeroportos[voo.origin]
                csv+='",-\n'

            csv+="Voo "+voo.origin+'-'+voo.destination + ' ' + voo.activity_info
            if voo.duty_design:
                csv+=" (E)"

            csv+=","
            csv += voo.sta.strftime('%m/%d/%Y')+","
            csv += voo.sta.strftime('%H:%M')+","
            csv+=voo.std.strftime('%m/%d/%Y')+","
            csv += voo.std.strftime('%H:%M')+","

            csv+='False,"'
            if voo.origin in aeroportos:
                csv+=aeroportos[voo.origin]

            csv+='",Horas de voo: '
            csv+=voo.horas_de_voo

            csv += '\n'

        return csv

    def get_numero_voos(self):
        return len(self.escalas)

    def somaHoras(self):
        segundos = 0

        for voo in self.escalas:
            codigos_voo = ['FR', 'REU', 'R04', 'R05', 'R06', 'R07', 'R08',
                            'R09', 'R12', 'R13', 'R15', 'R18', 'R21',
                            'P01', 'P02', 'P03','P04', 'P05', 'P06', 'P07',
                            'P08', 'P09', 'P10', 'P11',
                            'RHC', 'PLT', 'S04', 'S05', 'S06',
                            'P12','S12', 'S20', 'R0', 'FP', 'F']

            if voo.activity_info not in codigos_voo and not voo.duty_design:
                delta = voo.std - voo.sta

                segundos += delta.seconds

        minutos = segundos / 60
        return  minutos

class Voo:
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
    print "<html><body>"
    print "<span>"+VERSION+"</span>"
    print '<form action="escala.py" method="post" enctype="multipart/form-data">'
    print 'Upload file: <input type="file" name="myfile" /> <br />'
    print ' <input type="submit" name="submit" value="Submit" />'
    print ' </form>'
    try:
        import cgi
        form_data = cgi.FieldStorage()

        file_data = None
        if 'myfile' in form_data:
            file_data = form_data['myfile'].value
        else:
            if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
                xml = sys.argv[1]
            else:
                xml = 'escala.xml'
            if os.path.exists(xml):
                f = open(xml)
                file_data = f.read()

        if file_data:
            escala = Escala(string_xml = file_data)

            output = escala.csv()

            tmp_escala = 'tmp/escala.csv'
            if os.path.exists(tmp_escala):
                os.remove(tmp_escala)

            f = open(tmp_escala, 'w+')
            f.write(output)
            f.close()

            print "<p>Horas de voo: "+ str(escala.somaHoras()/60) + "</p>"
            print "<pre>" + output + "</pre>"
    except:
        import sys
        print "Unexpected error:", sys.exc_info()[1]
        print traceback.format_exc()


    if 'myfile' in form_data:
        print "<a href='"+tmp_escala+"'>escala.csv</a>"

    print "</body></html>"
