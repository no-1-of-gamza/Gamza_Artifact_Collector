# -*- coding: utf-8 -*-
import print_message
from option import option_set

from Artifact.a_recyclebin_data import RecycleBin
from Artifact.a_system_information import Systeminfo_Collector
from Artifact.a_registry_data import Registry_config, Registry_Collector
from Artifact.a_event_log import EventLog_Config, EventLog_Collector
from Artifact.a_browser_history import Browser_Config, Browser_Collector
from Artifact.a_extension import Extension

from datetime import datetime
import os
import argparse
import multiprocessing
import traceback


def Browser_History(inspect_path, Window_version, InstallPath_system_root, profile_list, UTC):
    try:
        os.mkdir(f"{inspect_path}//Browser_History")
        Browser_History_result_path = str(inspect_path) + "\\Browser_History"

        Browser_config = Browser_Config(Window_version, InstallPath_system_root, profile_list)
        Browser_artifact_path = Browser_config.run()

        Browser_collector = Browser_Collector(Browser_History_result_path, UTC)
        Browser_collector.collect(Browser_artifact_path)
        print("Browser history...complete")
    except Exception as e:
        print(e)
        pass


def Event_log(inspect_path, Window_version, InstallPath_system_root, UTC):
    try:
        os.mkdir(f"{inspect_path}//Event")

        Event_log_result_path = str(inspect_path) + "\\Event"

        EventLog_config = EventLog_Config(Window_version, InstallPath_system_root)
        EventLog_artifact_path = EventLog_config.run()

        EventLog_collector = EventLog_Collector(Event_log_result_path, UTC)
        EventLog_collector.collect(EventLog_artifact_path)
        print("Event log...complete")
    except Exception as e:
        print(e)
        pass


def Registry_Data(inspect_path, Window_version, profile_list, UTC):
    try:
        os.mkdir(f"{inspect_path}//Registry")

        Register_result_path = str(inspect_path) + "\\Registry"

        Register_config = Registry_config(Window_version, profile_list)
        Resgister_artifact_path = Register_config.run()

        Register_collector = Registry_Collector(Register_result_path, UTC)
        Register_collector.collect(Resgister_artifact_path)
        print("Registry data...complete")
    except Exception as e:
        print(e)
        pass


def Recycle_bin(inspect_path, UTC):
    try:
        os.mkdir(f"{inspect_path}//Recycle_bin")
        Trashbin_result_path = str(inspect_path) + "\\Recycle_bin"

        artifact = RecycleBin(Trashbin_result_path, UTC)
        artifact.check_drive()

        artifact.collect()
        with multiprocessing.Pool(processes=4) as pool:
            pool.map(artifact.dump, artifact.src_dst)
        print("Recycle bin data...complete")

    except Exception as e:
        print(e)
        pass


def Extension_files(inspect_path, UTC, target_extensions):
    os.mkdir(f"{inspect_path}//Extension_file")
    Extension_files_result_path = str(inspect_path) + "\\Extension_file"

    Extension_files_artifact = Extension(Extension_files_result_path, UTC, target_extensions)
    Extension_files_artifact.create_dir(Extension_files_artifact.drive_list)
    Extension_files_artifact.collect()
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(Extension_files_artifact.dump, Extension_files_artifact.src_dst)

    print("Extension files...complete")


def main():
    try:
        # Welcome message
        print_message.print_welcome_message()

        # Load options
        args = option_set()

        # Enter Inspector and Victim names
        print("\nPlease Insert Inspector name")
        Inspector_name = input("Inspector name: ")
        Victim_name = input("Victim name: ")

        if Inspector_name == "":
            print("Inspector name is none")
            Inspector_name = "unknown"
        if Victim_name == "":
            print("Victim name is none")
            Victim_name = "unknown"

        # Current time
        date_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        # Folder creation time
        date_time_save_folder = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")

        print(f"Current Time: {date_time}")

        # Folder creation
        current_dir = os.getcwd()
        print(f"Made folder {current_dir}")
        print(f"Folder name: {date_time_save_folder}_{Inspector_name}_{Victim_name}")
        inspect_path = f"{date_time_save_folder}_{Inspector_name}_{Victim_name}"
        os.mkdir(f"{inspect_path}")

        # Collect system information artifact (default)
        system_information_collector = Systeminfo_Collector(inspect_path)
        system_information = system_information_collector.collect()

        UTC = system_information['Timezone']
        Window_version = system_information["ProductName"]
        InstallPath_system_root = system_information["InstallPath"]
        profile_list = system_information["UserProfile"]

        print("\nPlease Choose and Insert Option Collecting Artifact [1] or Collecting Specific Extension File [2]")
        function_choice = input("Function:")
        artifact = []
        target_extensions = []

        if function_choice == "":
            print("All of Artifact Collecting...")
            artifact = None

        elif function_choice == "1":
            
            print("Insert Collecting Artifact you want")
            input_artifact = input("Artifact: ")
            artifact = input_artifact.split()
            print(artifact)

        elif function_choice == "2":
            
            print("Insert Collecting File you want")
            target_extensions_input = input("File extension: ")
            target_extensions = target_extensions_input.split()
            print(target_extensions)
            if not target_extensions:
                print("No file extension entered")

        # Collect all default artifacts if no specific options are provided
        if (artifact is None or artifact==[]) and (target_extensions ==[] or target_extensions is None):
            print("All of Artifact Collecting...")
            Browser_History(inspect_path, Window_version, InstallPath_system_root, profile_list, UTC)
            Event_log(inspect_path, Window_version, InstallPath_system_root, UTC)
            Registry_Data(inspect_path, Window_version, profile_list, UTC)
            Recycle_bin(inspect_path, UTC)

        elif artifact:

            try:
                if 'b' in artifact:
                    Browser_History(inspect_path, Window_version, InstallPath_system_root, profile_list, UTC)
                if 'e' in artifact:
                    Event_log(inspect_path, Window_version, InstallPath_system_root, UTC)
                if 'r' in artifact:
                    Registry_Data(inspect_path, Window_version, profile_list, UTC)
                if 't' in artifact:
                    Recycle_bin(inspect_path, UTC)

            except Exception as e:
                pass

        if target_extensions:
            Extension_files(inspect_path, UTC, target_extensions)

        print("Success All Task")
        input("Press Enter to exit the program.")

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())
        input("Press Enter to exit the program.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
