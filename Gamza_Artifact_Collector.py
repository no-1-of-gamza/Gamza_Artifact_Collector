#-*- coding: utf-8 -*-
import print_message
from option import option_set
from Artifact.a_browser_history import browser_history
from Artifact.a_trash_bin_data import trashbin_data

from Artifact.a_system_information import Systeminfo_Collector
from Artifact.a_registry_data import Registry_config, Registry_Collector
from Artifact.a_event_log import EventLog_Config, EventLog_Collector

from datetime import datetime
import os
import argparse
import multiprocessing
import traceback


def main():
    try:
        #웰컴메세지
        print_message.print_welcome_message()

        #옵션불러오기
        args = option_set()

        #수사자, 사건 케이스 이름입력
        print("\nPlease Insert Inspector name")
        Inspector_name=input("Inspector_name: ")
        Victim_name=input("Victim_name: ")

        if Inspector_name =="":
            print("Ispector name is none")
            Inspector_name="unknown"
        if Victim_name =="":
            print("Victim name is none")
            Victim_name="unknown"

        #현재시간
        date_time=datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        #폴더 생성시간 
        date_time_save_folder=datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        
        print(f"Current Time: {date_time}")

        #py. 경로에 폴더생성
        current_dir=os.getcwd()
        print(f"Maked folder {current_dir}")
        print(f"Folder name: {date_time_save_folder}_{Inspector_name}_{Victim_name}")
        inspect_path=f"{date_time_save_folder}_{Inspector_name}_{Victim_name}"
        os.mkdir(f"{inspect_path}")

        artifact=args.artifact
        search_file=args.search
        #system infomation 아티팩트 불러오기 (기본)
        system_infomation_collector = Systeminfo_Collector(inspect_path)
        system_infomation = system_infomation_collector.collect()

        user_name=[system_infomation['ComputerName']]
        UTC=system_infomation['Timezone']
        Window_version = system_infomation["ProductName"]
        InstallPath_system_root = system_infomation["InstallPath"]


        if artifact is None:
            #Browser_History
            browser_history()

            #Event_Log
            os.mkdir(f"{inspect_path}//Event")
  
            Event_log_result_path = str(inspect_path) + "\\Event"
            
            EventLog_config = EventLog_Config(Window_version, InstallPath_system_root)
            EventLog_artifact_path = EventLog_config.run()

            EventLog_collector = EventLog_Collector(Event_log_result_path, UTC)
            EventLog_collector.collect(EventLog_artifact_path)

            #Register_Data
            os.mkdir(f"{inspect_path}//Registry")

            Register_result_path = str(inspect_path) + "\\Registry"
            
            Register_config = Registry_config(Window_version, user_name)
            Resgister_artifact_path = Register_config.run()

            Register_collector = Registry_Collector(Register_result_path, UTC)
            Register_collector.collect(Resgister_artifact_path)

            #Trashbin_Data      
            trashbin_data()
        elif artifact is True:
            if "b" in artifact :
                browser_history()
                
            if "e" in artifact:
                print("Event")

            if "r" in artifact:        
                print("Register")
            if "t" in artifact:
                trashbin_data()

        #Extension
        if search_file is True:
            if "doc" in search_file :
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

        print("오류가발생했습니다:")
        print(traceback.format_exc())
        os.system('pause')
        input("엔터 키를누르면 프로그램을종료합니다.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
