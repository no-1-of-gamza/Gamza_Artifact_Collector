# -*- coding: utf-8 -*-
import optparse

def option_set():
    parser = optparse.OptionParser(description="Gamza Scanner Artifact Collector")
    parser.add_option("-a", "--artifact", action="store", type="string", dest="artifact", help="Values after -a option for Artifact Section")

    parser.add_option("-s", "--search", action="store", type="string", dest="search", help="Search Filename Extension:")

    '''
    python Gamza_Artifact_Collector.py 
    '''
    return parser.parse_args()
