# -*- coding: utf-8 -*-
import print_message
from option import option_set

from a_recyclebin_data import RecycleBin
from a_system_information import Systeminfo_Collector
from a_registry_data import Registry_config, Registry_Collector
from a_event_log import EventLog_Config, EventLog_Collector
from a_browser_history import Browser_Config, Browser_Collector
from a_extension import Extension

from datetime import datetime
import os
import argparse
import multiprocessing
import traceback


def Browser_History(inspect_path, Window_version, InstallPath_system_root, profile_list, UTC):
    try:
        os.mkdir("%s//Browser_History" % inspect_path)
        Browser_History_result_path = str(inspect_path) + "\\Browser_History"

        Browser_config = Browser_Config(Window_version, InstallPath_system_root, profile_list)
        Browser_artifact_path = Browser_config.run()

        Browser_collector = Browser_Collector(Browser_History_result_path, UTC)
        Browser_collector.collect(Browser_artifact_path)
        print "Browser history...complete"
    except Exception as e:
        print e
        pass


def Event_log(inspect_path, Window_version, InstallPath_system_root, UTC):
    try:
        os.mkdir("%s//Event" % inspect_path)

        Event_log_result_path = str(inspect_path) + "\\Event"

        EventLog_config = EventLog_Config(Window_version, InstallPath_system_root)
        EventLog_artifact_path = EventLog_config.run()

        EventLog_collector = EventLog_Collector(Event_log_result_path, UTC)
        EventLog_collector.collect(EventLog_artifact_path)
        print "Event log...complete"
    except Exception as e:
        print e
        pass


def Registry_Data(inspect_path, Window_version, profile_list, UTC):
    try:
        os.mkdir("%s//Registry" % inspect_path)

        Register_result_path = str(inspect_path) + "\\Registry"

        Register_config = Registry_config(Window_version, profile_list)
        Resgister_artifact_path = Register_config.run()

        Register_collector = Registry_Collector(Register_result_path, UTC)
        Register_collector.collect(Resgister_artifact_path)
        print "Registry data...complete"
    except Exception as e:
        print e
        pass


def Recycle_bin(inspect_path, UTC):
    try:
        os.mkdir("%s//Trash_bin" % inspect_path)
        Trashbin_result_path = str(inspect_path) + "\\Trash_bin"

        artifact = RecycleBin(Trashbin_result_path, UTC)
        artifact.check_drive()

        artifact.collect()

        pool = multiprocessing.Pool(processes=4)
        pool.apply_async(artifact.dump)
        print "Recycle bin data...complete"
        pool.close()
        pool.join()
    except Exception as e:
        print e
        pass


def Extension_files(inspect_path, UTC, target_extensions):
    os.mkdir("%s//Extension_file" % inspect_path)
    Trashbin_result_path = str(inspect_path) + "\\Extension_file"

    Extension_files_artifact = Extension(Trashbin_result_path, UTC, target_extensions)
    Extension_files_artifact.create_dir(Trashbin_result_path, Extension_files_artifact.drive_list)
    Extension_files_artifact.collect()
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(Extension_files_artifact.dump, Extension_files_artifact.src_dst)

    print "Extension files...complete"


def main():
    try:
        # Welcome message
        print_message.print_welcome_message()

        # Load options
        args = option_set()

        # Enter Inspector and Victim names
        print "\nPlease Insert Inspector name"
        Inspector_name = raw_input("Inspector name: ")
        Victim_name = raw_input("Victim name: ")

        if Inspector_name == "":
            print "Inspector name is none"
            Inspector_name = "unknown"
        if Victim_name == "":
            print "Victim name is none"
            Victim_name = "unknown"

        # Current time
        date_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        # Folder creation time
        date_time_save_folder = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")

        print "Current Time: %s" % date_time

        # Folder creation
        current_dir = os.getcwd()
        print "Made folder %s" % current_dir
        print "Folder name: %s_%s_%s" % (date_time_save_folder, Inspector_name, Victim_name)
        inspect_path = "%s_%s_%s" % (date_time_save_folder, Inspector_name, Victim_name)
        os.mkdir(inspect_path)

        # Collect system information artifact (default)
        system_information_collector = Systeminfo_Collector(inspect_path)
        system_information = system_information_collector.collect()

        UTC = system_information['Timezone']
        Window_version = system_information["ProductName"]
        InstallPath_system_root = system_information["InstallPath"]
        profile_list = system_information["UserProfile"]

        print "\nPlease Choose and Insert Option Collecting Artifact [1] or Collecting Specific Extension File [2]"
        function_choice = raw_input("Function:")
        artifact=[]
        target_extensions=[]
        if function_choice == "":
            print "All of Artifact Collecting..."
            artifact = None

        elif function_choice == "1":
            print "Insert Collecting Artifact you want"
            input_artifact = raw_input("Artifact: ")
            artifact = input_artifact.split()
            print artifact

        elif function_choice == "2":
            print "Insert Collecting File you want"
            target_extensions_input = raw_input("File extension: ")
            target_extensions = target_extensions_input.split()
            print target_extensions
            if not target_extensions:
                print "No file extension entered"

        # Collect all default artifacts if no specific options are provided
        if (artifact is None or not artifact) and target_extensions is None:
            print "All of Artifact Collecting..."
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

        print "Success All Task"
        raw_input("Press Enter to exit the program.")

    except Exception as e:
        print "An error occurred:"
        print traceback.format_exc()
        raw_input("Press Enter to exit the program.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
