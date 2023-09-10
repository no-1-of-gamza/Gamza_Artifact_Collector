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


def Browser_History(inspect_path,Window_version,InstallPath_system_root,profile_list,UTC):
    try:
            os.mkdir(f"{inspect_path}//Browser_History")
            Browser_History_result_path = str(inspect_path) + "\\Browser_History"

            Browser_config = Browser_Config(Window_version, InstallPath_system_root, profile_list)
            Browser_artifact_path = Browser_config.run()

            Browser_collector = Browser_Collector(Browser_History_result_path, UTC)
            Browser_collector.collect(Browser_artifact_path)   
            print("browser history..complete")     
    except Exception as e:
        print(e)
        pass

def Event_log(inspect_path,Window_version,InstallPath_system_root,UTC):
    try:
           # Event_Log
            os.mkdir(f"{inspect_path}//Event")

            Event_log_result_path = str(inspect_path) + "\\Event"

            EventLog_config = EventLog_Config(Window_version, InstallPath_system_root)
            EventLog_artifact_path = EventLog_config.run()

            EventLog_collector = EventLog_Collector(Event_log_result_path, UTC)
            EventLog_collector.collect(EventLog_artifact_path)
            print("event log..complete")
    except Exception as e:
        print(e)
        pass 

def Registry_Data(inspect_path,Window_version,profile_list,UTC):
    try:
            # Registry_Data
            os.mkdir(f"{inspect_path}//Registry")

            Register_result_path = str(inspect_path) + "\\Registry"

            Register_config = Registry_config(Window_version, profile_list)
            Resgister_artifact_path = Register_config.run()

            Register_collector = Registry_Collector(Register_result_path, UTC)
            Register_collector.collect(Resgister_artifact_path)
            print("registry data..complete")
    except Exception as e:
        print(e)
        pass 

def Recycle_bin(inspect_path,UTC):
    try:
        os.mkdir(f"{inspect_path}//Trash_bin")
        Trashbin_result_path = str(inspect_path) + "\\Trash_bin"

        artifact = RecycleBin(Trashbin_result_path, UTC)
        artifact.check_drive()

        artifact.collect()

        pool = multiprocessing.Pool(processes=4)
        pool.apply_async(artifact.dump)
        print("recycle bin data..complete")
        pool.close()
        pool.join()
    except Exception as e:
        print(e)
        pass 


def Extension_files(inspect_path,UTC,target_extensions):
    os.mkdir(f"{inspect_path}//Extension_file")
    Trashbin_result_path = str(inspect_path) + "\\Extension_file"

    Extension_files_artifact = Extension(Trashbin_result_path, UTC,target_extensions)
    Extension_files_artifact.create_dir(Trashbin_result_path, Extension_files_artifact.drive_list)
    Extension_files_artifact.collect()
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(Extension_files_artifact.dump, Extension_files_artifact.src_dst)
        
    print("Extension_files..complete")

def main():
    try:
        # 웰컴 메세지
        print_message.print_welcome_message()

        # 옵션 불러오기
        args = option_set()

        # 수사자, 사건 케이스 이름 입력
        print("\nPlease Insert Inspector name")
        Inspector_name = input("Inspector_name: ")
        Victim_name = input("Victim_name: ")

        if Inspector_name == "":
            print("Ispector name is none")
            Inspector_name = "unknown"
        if Victim_name == "":
            print("Victim name is none")
            Victim_name = "unknown"

        # 현재 시간
        date_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        # 폴더 생성 시간
        date_time_save_folder = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")

        print(f"Current Time: {date_time}")

        # 폴더 생성
        current_dir = os.getcwd()
        print(f"Made folder {current_dir}")
        print(f"Folder name: {date_time_save_folder}_{Inspector_name}_{Victim_name}")
        inspect_path = f"{date_time_save_folder}_{Inspector_name}_{Victim_name}"
        os.mkdir(f"{inspect_path}")

        artifact = args.artifact
        target_extensions = args.file
        # 시스템 정보 아티팩트 불러오기 (기본)
        system_information_collector = Systeminfo_Collector(inspect_path)
        system_information = system_information_collector.collect()

        UTC = system_information['Timezone']
        Window_version = system_information["ProductName"]
        InstallPath_system_root = system_information["InstallPath"]
        profile_list = system_information["UserProfile"]

        #프로그램 기본값 아티팩트 모두 수집
        if artifact is None and target_extensions is None:
            print("All of Artifact Collecting...")
            Browser_History(inspect_path,Window_version,InstallPath_system_root,profile_list,UTC)
            Event_log(inspect_path,Window_version,InstallPath_system_root,UTC)
            Registry_Data(inspect_path,Window_version,profile_list,UTC)
            Recycle_bin(inspect_path,UTC)

        elif artifact:
            try:
                if 'b' in artifact:
                    Browser_History(inspect_path,Window_version,InstallPath_system_root,profile_list,UTC)
                if 'e' in artifact:
                    Event_log(inspect_path,Window_version,InstallPath_system_root,UTC)  
                if 'r' in artifact:
                    Registry_Data(inspect_path,Window_version,profile_list,UTC)
                if 't' in artifact:
                    Recycle_bin(inspect_path,UTC)

            except Exception as e :
                pass

        if target_extensions:
            Extension_files(inspect_path, UTC, target_extensions)
        
        print("Success All Task")
        input("엔터 키를 누르면 프로그램을 종료합니다.")

    except Exception as e:
        print("오류가 발생했습니다:")
        print(traceback.format_exc())
        input("엔터 키를 누르면 프로그램을 종료합니다.")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
