import print_message
from option import option_set
from Artifact.a_browser_history import browser_history
from Artifact.a_event_log import event_log
from Artifact.a_resistry_data import resistry_data
from Artifact.a_trash_bin_data import trashbin_data

from Artifact.a_system_information import Systeminfo_Collector
from Artifact.a_resistry_data import Registry_config, Registry_Collector


from datetime import datetime
import os
import argparse

def main():
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
    print(f"File name: {date_time_save_folder}_{Inspector_name}_{Victim_name}")
    new_inspect=os.mkdir(f"{date_time_save_folder}_{Inspector_name}_{Victim_name}")
    # 새로운 폴더로 이동
    os.rename(current_dir, os.path.join(current_dir, new_inspect))

    artifact=args.artifact
    search_file=args.search

    #system infomation 아티팩트 불러오기 (기본)
    system_infomation = Systeminfo_Collector()
    user_name=system_infomation.collect_systeminfo["ComputerName"]
    UTC=system_infomation.collect_timezone["Timezone"]
    Window_version = system_infomation.collected_info["ProductName"]


    if artifact is False:
        #Browser_History
        browser_history()

        #Event_Log
        event_log()

        #Resigter_Data

        Register_config = Registry_config(Window_version, user_name)
        Resgister_artifact_path = Register_config.run()
        Register_collector = Registry_Collector(UTC)
        Register_collector.collect(Resgister_artifact_path)

        #Trashbin_Data      
        trashbin_data()
    elif artifact is True:
        if "b" in artifact :
            browser_history()
            
        if "e" in artifact:
            event_log()

        if "r" in artifact:        
            Register_config = Registry_config(Window_version, user_name)
            Resgister_artifact_path = Register_config.run()
            Register_collector = Registry_Collector(UTC)
            Register_collector.collect(Resgister_artifact_path)

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



if __name__ == "__main__":
    main()
