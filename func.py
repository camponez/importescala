import os
import xml.etree.ElementTree as ET

def load_xml(arquivo_xml):
    """
    Load xml
    """
    if not os.path.exists(arquivo_xml):
        print('Oh dear: ' + arquivo_xml + ' not found')
        raise

    tree = ET.parse(arquivo_xml)
    root = tree.getroot()

    return root

def load_string_xml(string_xml):
    """
    Loading string
    """
    root = ET.fromstring(string_xml)

    return root
def strfdate(date):
    """
    Converter data pra string
    """
    return date.strftime('%d/%m/%Y')

def strfdate_ics(date):
    """
    Converter data ics pra string
    """
    return date.strftime('%Y%m%d')

def format_date(voo):
    """
    Formatar data
    """
    string = strfdate(voo.sta) + ","
    string += voo.sta.strftime('%H:%M') + ","
    string += strfdate(voo.std) + ","
    string += voo.std.strftime('%H:%M') + ","
    return string

def format_date_ics(voo, checkin=False):
    """
    Formatar data for ICS
    """
    if checkin:
        string = "DTSTAMP:" + strfdate_ics(voo.activity_date)
        string += "T" + voo.checkin_time.strftime('%H%M00Z') + "\n"

        string += "DTSTART:" + strfdate_ics(voo.activity_date)
        string += "T" + voo.checkin_time.strftime('%H%M00Z') + "\n"

        string += "DTEND:" + strfdate_ics(voo.activity_date)
        string += "T" + voo.checkin_time.strftime('%H%M00Z') + "\n"
    else:
        string = "DTSTAMP:" + strfdate_ics(voo.sta)
        string += "T" + voo.sta.strftime('%H%M00Z') + "\n"

        string += "DTSTART:" + strfdate_ics(voo.sta)
        string += "T" + voo.sta.strftime('%H%M00Z') + "\n"

        string += "DTEND:" + strfdate_ics(voo.std)
        string += "T" + voo.std.strftime('%H%M00Z') + "\n"

    return string

# vim:tabstop=4:expandtab:smartindent
