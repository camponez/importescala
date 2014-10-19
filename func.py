import os
import xml.etree.ElementTree as ET

def load_xml(arquivo_xml):
    """
    Load xml
    """
    if not os.path.exists(arquivo_xml):
        print 'Oh dear: ' + arquivo_xml + ' not found'
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

def format_date(voo):
    """
    Formatar data
    """
    string = strfdate(voo.sta) + ","
    string += voo.sta.strftime('%H:%M') + ","
    string += strfdate(voo.std) + ","
    string += voo.std.strftime('%H:%M') + ","
    return string

# vim:tabstop=4:expandtab:smartindent
