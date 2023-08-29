import print_message
from option import option_set
from a_browser_history import browser_history
from a_event_log import event_log
from a_resistry_data import resistry_data
from a_system_information import system_information
from a_trash_bin_data import trashbin_data


from datetime import datetime
import os
import argparse

def main():
    print_message.print_welcome_message()

    args = option_set()

    print("\nPlease Insert Inspector name")
    Inspector_name=input("Inspector_name: ")
    Victim_name=input("Victim_name: ")

    if Inspector_name =="":
        print("Ispector name is none")
        Inspector_name="unknown"
    if Victim_name =="":
        print("Victim name is none")
        Victim_name="unknown"

    date_time=datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    date_time_save_folder=datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    
    print(f"Current Time: {date_time}")

    current_dir=os.getcwd()
    print(f"Maked folder {current_dir}")
    print(f"File name: {date_time_save_folder}_{Inspector_name}_{Victim_name}")
    os.mkdir(f"{date_time_save_folder}_{Inspector_name}_{Victim_name}")

    artifact=args.artifact
    print(artifact)

    if artifact is False:
        browser_history()
        event_log()
        resistry_data()
        system_information()
        trashbin_data()
    else :
        if "b" in artifact :
            browser_history()
        if "e" in artifact:
            event_log()
        if "r" in artifact:
            resistry_data()
        if "i" in artifact:
            system_information()
        if "t" in artifact:
            trashbin_data()


if __name__ == "__main__":
    main()
