#!/usr/bin/python
#  gwd.py get weather historical data about region of Lazio, in Italy
#
#    source is the Hydrographic and Mareographic Office 
#    (http://www.idrografico.roma.it/default.aspx) of Regione Lazio
#    (http://www.regione.lazio.it/rl_main/) of Italy.
#    Annals are at: 'http://www.idrografico.roma.it/annali/'
#
#  author:  luciano de falco alfano
#  license: CC by 4.0 (https://creativecommons.org/licenses/by/4.0/)
#  history:
#    - 2018-02-15, ver.1.0, 1st release, output weather data about a
#                           meteo station, given a year. it's an html page
#    - 2018-02-25, ver.1.1, added -t option to output only the yearly
#                           total precipitation

__version__ = '1.1'

help = '''
gwd.py - get weather historical data about Lazio region in Italy

use: python gwd.py {{-h | -l | -s STATION -y YEAR }} {{-t}}
    - h        print this help
    - l        print valid stations names
    - s        STATION is a valid weather station name in Lazio
                    e.g. ACILIA; in case of space in name, surround it by
                    quote e.g. "ACQUA ACETOSA"
    - y        YEAR is the request year, in the form YYYY
                    tipically from 2003 to 2017 (at the date of Feb 2018)
    - t        output only the yearly total precipitation

output is html send to stdout; redirect it to file if you wish

version is {}
'''.format(__version__)

#import pdb
import os
import sys
import csv
import getopt
import requests             # used to send a POST request to web server
from lxml import etree      # in case of html parsing necessity
from io import StringIO, BytesIO


VALID_STATIONS = [
    "ABBAZIA TRISULTI",  # km 73 mountain
    "ACILIA",            # 15 suburb
    "ACQUA ACETOSA",     #  5 town
    "ALATRI",            # 73 hilly
    "ALLUMIERE",         # 56 hilly
    "ANTRODOCO",
    "ANZIO",
    "APRILIA",
    "ARDEA",
    "ARSOLI",
    "ATINA",
    "AURELIO",
    "BACCANO",
    "BAGNOREGIO",
    "BARBARANO",
    "BOLSENA",
    "BORGO MONTELLO",
    "BORGO S.MARIA",
    "BORGOROSE",
    "BOVILLE ERNICA",
    "BRACCIANO",
    "BRUSCIANO",
    "CAMPO DI CARNE",
    "CAMPOLI APPENNINO",  # 100 mountains
    "CANINO RLAZIO",
    "CAPANNACCE",
    "CASILINO",
    "CASSINO",
    "CASSIODORO",
    "CASTEL CELLESI",
    "CASTELGIUBILEO",
    "CASTELLO VICI",
    "CECCANO RLAZIO",
    "CECCHINA",
    "CEPRANO",
    "CERVARO",
    "CERVETERI",
    "CISTERNA DI LATINA",
    "CITTADUCALE",
    "CITTAREALE",
    "CIVITA CASTELLANA",
    "CIVITAVECCHIA",
    "COLLALTO SABINO",
    "COLLEFERRO",
    "COLLEGIO ROMANO",
    "COLLI SUL VELINO",
    "CORCHIANO",
    "CORI",
    "ELENIANO",
    "ESPERIA",
    "EUR",
    "FALCOGNANA",
    "FERENTINO",
    "FIANO ROMANO",
    "FIDENE",
    "FILETTINO",
    "FIUGGI",
    "FLAMINIO",
    "FONDI",
    "FONTANA LIRI SUPERIORE",
    "FORMELLO",
    "FOSSANOVA",
    "FRASCATI",
    "FREGENE",
    "FROSINONE",
    "GAETA",               # 117 longshore
    "GIULIANO DI ROMA",
    "GUIDONIA",
    "ISCHIA DI CASTRO",
    "ISOLA SACRA",         # 26 longshore/suburb
    "ITRI",
    "LA STORTA",
    "LADISPOLI RLAZIO",    # 35 longshore
    "LAGO DI ALBANO",
    "LAGO DI NEMI",
    "LANUVIO",
    "LATINA",
    "LENOLA",
    "LEONESSA",            # 83 mountains
    "LICENZA",
    "LUGNANO",
    "LUNGHEZZA",
    "MACCARESE",
    "MACCARESE RLAZIO",
    "MANDRIONE",
    "MANZIANA",
    "MARANO EQUO",
    "MARTA",
    "MASSIMINA",
    "MICIGLIANO",
    "MIGNONE",
    "MONTALTO DI CASTRO",
    "MONTASOLA",
    "MONTE MARIO",
    "MONTE ROMANO",
    "MONTE TERMINILLO",
    "MONTEFIASCONE",
    "MONTELIBRETTI",
    "MONTEROTONDO ETG",
    "MORICONE",
    "MORLUPO",
    "NEPI",
    "NEROLA",
    "NORMA",
    "ORTE SCALO",
    "OSTERIA DI CASTRO",
    "OSTERIA NUOVA",
    "OSTIA",
    "OSTIA PANTANELLO",
    "OSTIENSE",
    "OTTAVIA",
    "PAGLIA A PROCENO",
    "PALESTRINA",
    "PALIANO",
    "PALOMBARA SABINA",
    "PASSO CORESE ETG",
    "POGGIO MIRTETO",
    "POMEZIA",
    "PONTE FELICE",
    "PONTE FERRAIOLI",
    "PONTE GALERIA ACEA",
    "PONTE SALARIO",
    "PONTECORVO",
    "PONZA",
    "PORTA PORTESE",
    "POSTA",
    "POSTICCIOLA",
    "PRATOLUNGO",
    "PRIVERNO",
    "REGILLO",
    "RIANO",
    "RIETI IDRO",
    "RIGNANO FLAMINIO",
    "RIO CASSANO",
    "RIPI",
    "RIVODUTRI",
    "ROCCA DI PAPA",
    "ROCCA RESPAMPANI",
    "ROCCA SINIBALDA",
    "ROCCASECCA",
    "ROMA BUFALOTTA",
    "ROMA EST",
    "ROMA EUR",
    "ROMA FLAMINIO",
    "ROMA MACAO",
    "ROMA MONTE MARIO",
    "ROMA NORD",
    "ROMA SUD",
    "RONCIGLIONE RLAZIO",
    "ROSOLINO PILO",
    "ROTA",
    "ROVIANO",
    "S.ANGELO THEODICE",
    "S.APOLLINARE RLAZIO",
    "S.VITO ROMANO",
    "SABAUDIA",                 # 80 longshore
    "SALISANO",
    "SALONE",
    "SAN BIAGIO SARACINISCO",
    "SAN MARTINO",
    "SANTA SEVERA",
    "SASSO FURBARA",
    "SETTEFRATI",
    "SEZZE",
    "SGURGOLA",
    "SORA",
    "SORGENTI CAPORE",
    "SORGENTI PESCHIERA",
    "SORIANO NEL CIMINO",
    "SPIGNO SATURNIA",
    "SS.COSMA E DAMIANO",
    "STIMIGLIANO",
    "SUBIACO",
    "SUBIACO-SCOLASTICA",
    "SUTRI",
    "TAFONE",
    "TARQUINIA",
    "TERRACINA",
    "TIVOLI",
    "TOR MARANCIA",
    "TOR VERGATA",
    "TORRITA TIBERINA",
    "TRAGLIATELLA RLAZIO",
    "TREVI NEL LAZIO",
    "TREVIGNANO ROMANO",
    "TUSCANIA",
    "VALENTANO",
    "VALLECORSA",
    "VELLETRI",
    "VEROLI",
    "VIA MARCHI",
    "VITERBO",
    "VIVARO ROMANO",
    "VULCI",
    "ZAGAROLO",
    ]


VALID_YEARS = [
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017"]


# defining the api-endpoint 
API_ENDPOINT = 'http://www.idrografico.roma.it/annali/home.asp'
#STAZIONE = 'ACILIA'
#ANNO = '2003'
MESE = '0'                 # 0: all months of the indicated year
SENSORI = 'pluviometri'    # getting only rain gauge data

PRINT_HELP  = False
PRINT_VALID_STATIONS = False
STATION     = ''
YEAR        = ''
YEARLY_ONLY = False

def check_cmd(argv):
    '''check command line arguments'''
    
    global PRINT_HELP
    global PRINT_VALID_STATIONS
    global STATION
    global YEAR
    global YEARLY_ONLY
    
    rc = -1
    try:
       opts, args = getopt.getopt(argv,"hls:y:t",[])
    except getopt.GetoptError:
       print(help)
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          PRINT_HELP = True
       elif opt in ("-l"):
          PRINT_VALID_STATIONS = True
       elif opt in ("-s"):
          STATION = arg
       elif opt in ("-y"):
          YEAR = arg
       elif opt == '-t':
          YEARLY_ONLY = True
    if (STATION \
          and STATION in VALID_STATIONS \
        and YEAR \
          and YEAR in VALID_YEARS) \
       or PRINT_HELP \
       or PRINT_VALID_STATIONS:
       rc = 0
    return rc


def get(station, year):
    '''get station/year weather data by POST request
    
    return html response got from server
    '''
    
    # data to be sent to api
    data = {'stazione': station,
            'anno':     year,
            'mese':     MESE,
            'sensori':  SENSORI}
    
    r = requests.post(url = API_ENDPOINT, data = data)  # sending post request
    resp = r.text                                    # extracting response text 
    return resp

def get_yearly(response):
    '''from html page get yearly total precipitation
    
    Remarks. Searched data is in a table cell(<td> ... </td>)
    containing text "Totale annuo: xxx,yy". Where xxx,yy is the searched
    number.
    
    return a float number as string
    '''
    result = None
    html   = etree.HTML(response)
    #pdb.set_trace()
    elems = html.xpath('.//td[starts-with(text(),"Totale annuo")]')
    if len(elems) == 1:
        result = elems[0].text
        result = result.split(' ')[-1]
        if ',' in result:
            result = result.replace('.', '')
            result = result.replace(',', '.')
    
    return result

def main():
    '''process commands'''
    
    if PRINT_HELP:
        print(help)
    elif PRINT_VALID_STATIONS:
        print('valid stations are:\n {}'.format(VALID_STATIONS))
    elif (STATION and YEAR):
        try:
            resp = get(STATION, YEAR)    # resp is a html webpage
            if YEARLY_ONLY:
                resp = get_yearly(resp)  # result is a float number as string
            print(resp)
        except:
            print('oops: something went wrong during the request of data')
            raise
    else:
        print('some kind of inexplicable error')
    return


if __name__ == "__main__":
    rc = check_cmd(sys.argv[1:])
    if rc == -1:
        print("error from cmd parameters. use -h to get help")
    else:
        main()