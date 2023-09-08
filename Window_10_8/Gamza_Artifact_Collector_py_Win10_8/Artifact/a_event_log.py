import os
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
import subprocess


class EventLog_Config:
    def __init__(self, version:str, system_root:str):
        self.artifact = ""
        self.version = version
        self.system_root = system_root


    def run(self) -> object:
        if "Windows 10" in self.version:
            self.artifact_Win10()
        elif "Windows 8" in self.version:
            self.artifact_Win8()
        elif "Windows 7" in self.version:
            self.artifact_Win7()
        elif "Windows XP" in self.version:
            self.artifact_WinXP()

        return self.artifact


    def artifact_Win10(self):
        self.artifact = self.system_root+"\\System32\\winevt\\Logs"


    def artifact_Win8(self):
        self.artifact = self.system_root+"\\System32\\winevt\\Logs"


    def artifact_Win7(self):
        self.artifact = self.system_root+"\\System32\\winevt\\Logs"


    def artifact_WinXP(self):
        self.artifact = self.system_root+"\\system32\\config"


class EventLog_Collector:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC

        self.collected_info = []


    def collect(self, artifact_path):
        dir_path = artifact_path
        file_list = os.listdir(dir_path)
        dump_list = []

        for file_name in file_list:
            extension = file_name.split(".")[-1].lower()
            if extension == "evtx" or extension == "evt":
                file_path = dir_path+"\\"+file_name

                self.collected_info.append(self.get_file_info(file_path))
                dump_list.append(file_path)

        self.collect_dump(dump_list)
        
        self.create_summary()


    def get_file_info(self, file_path) -> list:
        stat = os.stat(file_path)
        
        name = file_path.split("\\")[-1]
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size//1024 # KB

        info = [name, mtime, atime, ctime, size, file_path]
        return info


    def timestamp_to_UTC(self, timestamp) -> datetime:
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp))+utc_offset

        return utc_modify


    def create_summary(self):
        output = "EventLog     UTC+{}\n".format(self.UTC)
        output += "\n\n"

        strFormat = '%-40s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(KB)', 'Path']
        output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.collected_info:
            output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])

        with open(self.result_path+'\\summary.txt', 'w') as f:
            f.write(output)


    def collect_dump(self, dump_list):
        result_signal = Queue()
        process_list = []
        for path in dump_list:
            process = Process(target=self.dump_worker, args=(path, result_signal))
            process_list.append(process)
            process.start()

        for p in process_list:
            p.join()

        result = 0
        cnt = len(dump_list)
        while True:
            result += result_signal.get()
            if result >= cnt:
                print("dumping event log complete...")
                break


    def dump_worker(self, src_path, signal):
        dst_path = self.result_path
        try:
            subprocess.run(["RawCopy.exe", "/FileNamePath:"+src_path, "/OutputPath:"+dst_path])
        except Exception as e:
            print(e)

        signal.put(1)


# if __name__ == "__main__":
    
#     result_path = "D:\\Goorm\\Project_2\\code\\EventLog"
#     UTC = 9
#     system_root = "C:\\Windows"

#     start_time = time.time()

#     config = EventLog_Config("Windows 10 Pro", system_root)
#     artifact_path = config.run()

#     collector = EventLog_Collector(result_path, UTC)
#     collector.collect(artifact_path)

#     end_time = time.time()

#     print("complete")
#     print("time:", end_time-start_time)
