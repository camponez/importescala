#!/usr/bin/python
# coding=utf-8
print ("Content-type: text/html\n\n")

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

SEGUNDA = 0
TERCA = 1
QUARTA = 2
QUINTA = 3
SEXTA = 4
SABADO = 5
DOMINGO = 6


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
        self.simulador = ['S04', 'S05', 'S06', 'S12', 'S20', 'T30',
                          'SBO', 'H30']

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

        horas = Horas(self.escalas, self.ignore_list)

        horas.calc_saidas_chegadas()

        return  [horas.tempo_diurno_str, horas.tempo_noturno_str, horas.tempo_total_str,
                 horas.tempo_faixa2_str]

class Horas(object):
    "Classe Horas"
    def __init__(self, escalas, ignore_list):
        self.escalas = escalas
        self.ignore_list = ignore_list

        self.tempo_total_str = None
        self.tempo_noturno_str = None
        self.tempo_diurno_str = None
        self.tempo_diurno_especial_str = None
        self.tempo_faixa2_str = '0:00'
    # __init__()

    def calc_saidas_chegadas(self):
        """Cálculo de chegadas e saidas"""

        segundos_diurno_especial = 0
        segundos_diurno = 0
        segundos_noturno = 0
        segundos_noturno_especial = 0

        for voo in self.escalas:
            chegada_18h = self.calc_data(voo.std, 18, 0)

            chegada_6h = self.calc_data(voo.std, 6, 0) + timedelta(hours=24)

            saida_18h = self.calc_data(voo.sta, 18, 0)

            saida_6h = self.calc_data(voo.sta, 6, 0)

            if voo.activity_info not in self.ignore_list and \
               not voo.activity_info.startswith('R') and \
               not voo.duty_design:

                if voo.sta > saida_18h and voo.std < chegada_6h:
                    delta = voo.std - voo.sta
                    segundos_noturno += delta.seconds
                    continue

                if voo.sta > saida_6h and voo.std < chegada_18h:
                    delta = voo.std - voo.sta
                    segundos_diurno += delta.seconds

                    if voo.std.weekday() == DOMINGO:
                        segundos_diurno_especial += delta.seconds
                    continue

                if voo.sta > saida_18h and voo.std > chegada_6h or \
                        voo.sta > saida_18h and voo.std > saida_6h:
                    delta = voo.std - saida_18h
                    segundos_noturno += delta.seconds

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
        #tempo_noturno_especial = datetime(1, 1, 1) + \
        #        timedelta(seconds=segundos_noturno)

        tempo_total = datetime(1, 1, 1) + timedelta(seconds=segundos_total)

        self.tempo_diurno_str = self.calc_tempo_str(tempo_diurno)

        self.tempo_noturno_str = self.calc_tempo_str(tempo_noturno)

        self.tempo_total_str = self.calc_tempo_str(tempo_total)

        self.tempo_diurno_especial_str = self.calc_tempo_str(tempo_diurno_especial)

        if ((tempo_total.day - 1) * 24 + tempo_total.hour) > 70:
            self.tempo_faixa2_str = "%d:%02d" % \
                    ((tempo_total.day - 1) * 24 + tempo_total.hour - 70,
                     tempo_total.minute)

    # calc_saidas_chegadas()

    def calc_data(self, data, hora, minuto):
        return datetime(data.year,
                        data.month,
                        data.day,
                        hora, minuto)
    # calc_data()

    def calc_tempo_str(self, tempo):
        return "%d:%02d" % \
                ((tempo.day - 1) * 24 + tempo.hour,
                  tempo.minute)

    # calc_tempo()

class Voo(object):
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
    html = "<html><head>"
    html += "<meta http-equiv='Content-Type' content='text/html;charset=UTF-8'>"
    html += "</head><body>"
    html += "<table><tr><td>"
    html += open('how-to.html').read()
    html += "</td><td>"
    html += "<div style='text-align:center'><p>Changelog</p></div>"
    html += "<ul>"
    html += open('changelog.html').read()
    html += "</ul>"
    html += "</td></tr></table>"
    html += "<span>" + VERSION + "</span>"
    html += '<form action="escala.py" method="post" enctype="multipart/form-data">'
    html += 'Upload file: <input type="file" name="myfile" /> <br />'
    html += ' <input type="submit" name="submit" value="Submit" />'
    html += ' </form>'

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

            HORAS_DIURNO = ESCALA.soma_horas()[0]
            HORAS_NOTURNO = ESCALA.soma_horas()[1]
            HORAS_TOTAL = ESCALA.soma_horas()[2]
            HORAS_FAIXA_2 = ESCALA.soma_horas()[3]

            html +=  "<p>Horas de voo diurno: " + HORAS_DIURNO + "</p>"
            html +=  "<p>Horas de voo noturno: " + HORAS_NOTURNO + "</p>"
            html +=  "<p>Horas de voo total: " + HORAS_TOTAL + "</p>"
            html +=  "<p>Horas de voo Faixa 2: " + HORAS_FAIXA_2 + "</p>"
            if 'myfile' in FORM_DATA:
                html += "<a href='" + TMP_ESCALA + "'>escala.csv</a>"
            html += "<pre>" + OUTPUT + "</pre>"
    except:
        html += "Unexpected error:", sys.exc_info()[1]
        html += traceback.format_exc()


    ANALYTICS = "\
<script>\n\
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\n\
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n\
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n\
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');\n\
ga('create', 'UA-2271271-18', 'auto');\n\
ga('send', 'pageview');\n\
</script>\n\
"

    AMONG_US = '\
<script id="_waux0d">var _wau = _wau || [];\n\
_wau.push(["tab", "z9s00fhb7vfs", "x0d", "bottom-right"]);\n\
(function() {var s=document.createElement("script"); s.async=true;\n\
s.src="http://widgets.amung.us/tab.js";\n\
document.getElementsByTagName("head")[0].appendChild(s);\n\
})();</script>\n\
'


    html += ANALYTICS
    html += AMONG_US
    html += "</body></html>"
    print (html)

# vim:tabstop=4:expandtab:smartindent
