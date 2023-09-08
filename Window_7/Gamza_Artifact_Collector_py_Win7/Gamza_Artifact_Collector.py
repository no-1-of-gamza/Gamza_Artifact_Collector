# -*- coding: utf-8 -*-
import print_message
from option import option_set
from a_trash_bin_data import trashbin_data

from a_system_information import Systeminfo_Collector
from a_resistry_data import Registry_config, Registry_Collector
from a_browser_history import Browser_Config, Browser_Collector
from a_event_log import EventLog_Config, EventLog_Collector

from datetime import datetime
import os
import optparse
import multiprocessing
import traceback


def main():
    try:
        # 웰컴메세지
        print_message.print_welcome_message()

        # 옵션 불러오기
        parser = optparse.OptionParser(description="Gamza Scanner Artifact Collector")
        parser.add_option("-a", "--artifact", action="store_true", help="Use this option to collect specific artifacts.")
        parser.add_option("-s", "--search", action="store_true", help="Use this option to search for specific file extensions.")

        (options, args) = parser.parse_args()

        # 수사자, 사건 케이스 이름 입력
        print("\nPlease Insert Inspector name")
        Inspector_name = raw_input("Inspector_name: ")
        Victim_name = raw_input("Victim_name: ")

        if Inspector_name == "":
            print("Inspector name is none")
            Inspector_name = "unknown"
        if Victim_name == "":
            print("Victim name is none")
            Victim_name = "unknown"

        # 현재시간
        date_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        # 폴더 생성시간
        date_time_save_folder = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")

        print("Current Time: {}".format(date_time))

        # 현재 작업 디렉토리 경로에 폴더 생성
        current_dir = os.getcwd()
        print("Maked folder {}".format(current_dir))
        print("Folder name: {}".format(date_time_save_folder + "_" + Inspector_name + "_" + Victim_name))
        inspect_path = "{}".format(date_time_save_folder + "_" + Inspector_name + "_" + Victim_name)
        os.mkdir(inspect_path)

        artifact = options.artifact
        search_file = options.search

        # system information 아티팩트 불러오기 (기본)
        system_information_collector = Systeminfo_Collector(inspect_path)
        system_information = system_information_collector.collect()

        user_name=[system_information['ComputerName']]
        UTC=system_information['Timezone']
        Window_version = system_information["ProductName"]
        InstallPath_system_root = system_information["InstallPath"]
        profile_list= system_information["UserProfile"]


        if artifact is None:
            #Browser_History 
            os.mkdir("{0}//Browser_History".format(inspect_path))
            Browser_History_result_path = "{0}\\Browser_History".format(inspect_path)

            Browser_config = Browser_Config(Window_version, InstallPath_system_root, profile_list)
            Browser_artifact_path = Browser_config.run()

            Browser_collector = Browser_Collector(Browser_History_result_path, UTC)
            Browser_collector.collect(Browser_artifact_path)

            # Event_Log
            os.mkdir("{}/Event".format(inspect_path))

            Event_log_result_path = "{}/Event".format(inspect_path)

            EventLog_config = EventLog_Config(Window_version, InstallPath_system_root)
            EventLog_artifact_path = EventLog_config.run()

            EventLog_collector = EventLog_Collector(Event_log_result_path, UTC)
            EventLog_collector.collect(EventLog_artifact_path)

            # Register_Data
            os.mkdir("{}/Registry".format(inspect_path))

            Register_result_path = "{0}\\Registry".format(inspect_path)

            Register_config = Registry_config(Window_version, user_name)
            Resgister_artifact_path = Register_config.run()

            Register_collector = Registry_Collector(Register_result_path, UTC)
            Register_collector.collect(Resgister_artifact_path)

            # Trashbin_Data
            trashbin_data()
        elif artifact is True:
            if "b" in artifact:
                browser_history()

            if "e" in artifact:
                event_log()

            if "r" in artifact:
                print("Register")
            if "t" in artifact:
                trashbin_data()

        # Extension
        if search_file is True:
            if "doc" in search_file:
                print("doc")
            if "xls" in search_file:
                print("xls")
            if "txt" in search_file:
                print("txt")
            if "pdf" in search_file:
                print("pdf")
            if "zip" in search_file:
                print("zip")
            if "exe" in search_file:
                print("exe")
            if "lnk" in search_file:
                print("lnk")
    except Exception as e:
        print("오류가 발생했습니다:")
        print(traceback.format_exc())
        os.system('pause')
        raw_input("엔터 키를 누르면 프로그램을 종료합니다.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
