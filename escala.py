#!/usr/bin/python2
# -*- coding: utf-8 -*-
# coding=utf-8
import os
import traceback
import sys

from lib.escala import Escala

from __version__ import MINOR
from __version__ import MAJOR

print("Content-type: text/html\n\n")

VERSION = MAJOR + '.' + MINOR

if __name__ == "__main__":
    HTML = "<html><head>"
    HTML += "<meta http-equiv='Content-Type' content='text/html;charset=UTF-8'>"
    HTML += "</head><body>"
    HTML += "<table><tr><td>"
    HTML += open('how-to.html').read()
    HTML += "</td><td>"
    HTML += "<div style='text-align:center'><p>Changelog</p></div>"
    HTML += "<ul>"
    HTML += open('changelog.html').read()
    HTML += "</ul>"
    HTML += "</td></tr></table>"
    HTML += "<span>{}</span>".format(VERSION)
    HTML += '<form action="escala.py" method="post" enctype="multipart/form-data">'
    HTML += 'Upload file: <input type="file" name="myfile" /> <br />'
    HTML += ' <input type="submit" name="submit" value="Submit" />'
    HTML += ' </form>'

    try:
        import uuid
        import cgi
        FORM_DATA = cgi.FieldStorage()

        TMP_NAME = str(uuid.uuid4().get_hex().upper()[0:6])
        TMP_ESCALA_CSV = 'tmp/' + TMP_NAME + '.csv'

        TMP_NAME = str(uuid.uuid4().get_hex().upper()[0:6])
        TMP_ESCALA_ICS = 'tmp/' + TMP_NAME + '.ics'

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

            OUTPUT_CSV = ESCALA.csv()

            F = open(TMP_ESCALA_CSV, 'w+')
            F.write(OUTPUT_CSV)
            F.close()

            OUTPUT_ICS = ESCALA.ics()

            F = open(TMP_ESCALA_ICS, 'w+')
            F.write(OUTPUT_ICS)
            F.close()

            HTML += (
                "<p>Horas de voo diurno: {h_diurno}</p>"
                "<p>Horas de voo noturno: {h_noturno}</p>"
                "<p>Horas de voo total: {h_total_voo}</p>"
                "<p>Horas de voo Faixa 2: {h_faixa2}</p>"
                "<p>Horas de voo Sobreaviso: {h_sobreaviso}</p>"
                "<p>Horas de voo Reserva: {h_reserva}</p>"
                .format(**ESCALA.soma_horas())
            )
            if 'myfile' in FORM_DATA:
                HTML += "<a href='" + TMP_ESCALA_CSV + "'>escala.csv</a><br />"
                HTML += "<a href='" + TMP_ESCALA_ICS + "'>escala.ics</a>"
            HTML += "<pre>" + OUTPUT_CSV + "</pre>"
    except BaseException:
        HTML += "Unexpected error: {}".format(sys.exc_info()[1])
        HTML += traceback.format_exc()

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

    HTML += ANALYTICS
    HTML += AMONG_US
    HTML += "</body></html>"
    print(HTML)

# vim:tabstop=4:expandtab:smartindent
