import argparse
def option_set():
    parser = argparse.ArgumentParser(description="Gamza Scanner Artifact Collector")
    parser.add_argument("-a", "--artifact", nargs="+",help="Values after -a option for Artifact Section")

    parser.add_argument("-f","--file",nargs="+", help="Search Specific Extension File:")

    '''
    기본 사용법: python Gamza_Artifact_Collector.py 
    '''
    return parser.parse_args()