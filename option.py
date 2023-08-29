import argparse
def option_set():
    parser = argparse.ArgumentParser(description="Gamza Scanner Artifact Collector")
    parser.add_argument("-a","--artifact", action="store_true", help="Artifact Section:")

    parser.add_argument("-s","--search", action="store_true", help="Search Filename Extension:")

    '''
    기본 사용법: python Gamza_Artifact_Collector.py 
    '''
    return parser.parse_args()