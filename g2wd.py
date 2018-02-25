#!/usr/bin/python
#  g2wd.py get group of weather historical data about region of Lazio, in Italy
#
#    uses gwd.py, see it for documentation
#
#  author:  luciano de falco alfano
#  license: CC by 4.0 (https://creativecommons.org/licenses/by/4.0/)
#  history:
#    - 2018-02-25, ver.1.0, initial release

__version__ = '1.0'

help = '''
g2wd.py - get group of weather historical data about Lazio region in Italy

use: python g2wd.py 

configure in config.py

output is csv send to stdout; redirect it to file if you wish

version is {}
'''.format(__version__)

import pdb
import csv
import getopt
import os
import sys
import config as cfg
import gwd

PRINT_HELP = False

def check_cmd(argv):
    '''check command line arguments'''
    
    global PRINT_HELP
    
    try:
       opts, args = getopt.getopt(argv,"h",[])
    except getopt.GetoptError:
       print(help)
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          PRINT_HELP = True
    return None

def main():
    '''process commands'''
    
    if PRINT_HELP:
        print(help)
        return
    else:
        #pdb.set_trace()
        csvwriter = csv.writer(sys.stdout, lineterminator='\n')
        row = ["YEAR"]
        row.extend(cfg.STATIONS)
        csvwriter.writerow(row)
        for year in cfg.YEARS:
            row = [year]
            for station in cfg.STATIONS:
                response = gwd.get(station, year)
                response = gwd.get_yearly(response)
                row.append(response)
            csvwriter.writerow(row)
    return


if __name__ == "__main__":
    check_cmd(sys.argv[1:])
    main()
