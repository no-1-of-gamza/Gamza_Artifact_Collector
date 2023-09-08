# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
import subprocess


class Registry_config:
    def __init__(self, version, user_name):
        self.artifact = {}
        self.version = version
        self.user_name = user_name

    def run(self):
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
        self.artifact["registry"] = [
            "C:\\Windows\\System32\\config\\COMPONENTS",
            "C:\\Windows\\System32\\config\\DEFAULT",
            "C:\\Windows\\System32\\config\\DRIVERS",
            "C:\\Windows\\System32\\config\\SAM",
            "C:\\Windows\\System32\\config\\SECURITY",
            "C:\\Windows\\System32\\config\\SOFTWARE",
            "C:\\Windows\\System32\\config\\SYSTEM"
        ]

        self.artifact["ntuser"] = [
            "C:\\Windows\\SysWOW64\\config",
            "C:\\Users\\Default"
        ]
        self.artifact["usrclass"] = [
            "C:\\Windows\\SysWOW64\\config"
        ]

        self.artifact["amcache"] = "C:\\Windows\\appcompat\\Programs\\Amcache.hve"

    def artifact_Win8(self):
        self.artifact["registry"] = [
            "C:\\Windows\\System32\\config\\COMPONENTS",
            "C:\\Windows\\System32\\config\\DEFAULT",
            "C:\\Windows\\System32\\config\\DRIVERS",
            "C:\\Windows\\System32\\config\\SAM",
            "C:\\Windows\\System32\\config\\SECURITY",
            "C:\\Windows\\System32\\config\\SOFTWARE",
            "C:\\Windows\\System32\\config\\SYSTEM"
        ]

        self.artifact["ntuser"] = [
            "C:\\Users\\Default"
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\" + user)
            self.artifact["usrclass"].append("C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\Windows")

        self.artifact["amcache"] = "C:\\Windows\\AppCompat\\Programs\\Amcache.hve"

    def artifact_Win7(self):
        self.artifact["registry"] = [
            "C:\\Windows\\System32\\config\\COMPONENTS",
            "C:\\Windows\\System32\\config\\DEFAULT",
            "C:\\Windows\\System32\\config\\SAM",
            "C:\\Windows\\System32\\config\\SECURITY",
            "C:\\Windows\\System32\\config\\SOFTWARE",
            "C:\\Windows\\System32\\config\\SYSTEM"
        ]

        self.artifact["ntuser"] = [
            "C:\\Users\\Default"
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\" + user)
            self.artifact["usrclass"].append("C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\Windows")

        self.artifact["amcache"] = "C:\\Windows\\AppCompat\\Programs\\RecentFileCache.bcf"

    def artifact_WinXP(self):
        self.artifact["registry"] = [
            "C:\\Windows\\system32\\config\\default",
            "C:\\Windows\\system32\\config\\SAM",
            "C:\\Windows\\system32\\config\\SECURITY",
            "C:\\Windows\\system32\\config\\software",
            "C:\\Windows\\system32\\config\\system"
        ]

        self.artifact["ntuser"] = [
            "C:\\WINDOWS\\repair",
            "C:\\Documents and Settings\\Default User",  # caution: this path can't dump with this program
            "C:\\Documents and Settings\\Administrator"  # caution: this path can't dump with this program
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\" + user)
            self.artifact["usrclass"].append("C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\Windows")


class Registry_Collector:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC
        self.collected_info = []

    def collect(self, artifact_path):
        dump_list = []
        try:
            for path in artifact_path["registry"]:
                self.collected_info.append(self.get_file_info(path))
                dump_list.append(path)

            for dir_path in artifact_path["ntuser"]:
                user_profile_path = os.path.expanduser(dir_path)  # 사용자 프로파일 경로 가져오기
                if os.path.exists(user_profile_path):
                    file_list = os.listdir(user_profile_path)
                    for file_name in file_list:
                        if file_name.upper().endswith("NTUSER.DAT"):  # 대문자 변환 및 파일 확장자 검사
                            self.collected_info.append(self.get_file_info(os.path.join(user_profile_path, file_name)))
                            dump_list.append(os.path.join(user_profile_path, file_name))

            for dir_path in artifact_path["usrclass"]:
                user_profile_path = os.path.expanduser(dir_path)  # 사용자 프로파일 경로 가져오기
                if os.path.exists(user_profile_path):
                    file_list = os.listdir(user_profile_path)
                    for file_name in file_list:
                        if file_name.upper().endswith("USRCLASS.DAT"):  # 대문자 변환 및 파일 확장자 검사
                            self.collected_info.append(self.get_file_info(os.path.join(user_profile_path, file_name)))
                            dump_list.append(os.path.join(user_profile_path, file_name))

            self.collected_info.append(self.get_file_info(artifact_path["amcache"]))
            dump_list.append(artifact_path["amcache"])

            self.collect_dump(dump_list)

        except OSError:
            print("OSError occurred")

        self.create_summary()

    def get_file_info(self, file_path):
        stat = os.stat(file_path)
        name = file_path.split("\\")[-1]
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size // 1024  # KB

        info = [name, mtime, atime, ctime, size, file_path]
        return info

    def timestamp_to_UTC(self, timestamp):
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp)) + utc_offset

        return utc_modify

    def create_summary(self):
        output = "Registry     UTC+{}\n".format(self.UTC)
        output += "\n\n"

        strFormat = '%-30s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(KB)', 'Path']
        output += strFormat % (title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.collected_info:
            output += strFormat % (info[0], info[1], info[2], info[3], info[4], info[5])

        with open(self.result_path + '\\summary.txt', 'w') as f:
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
                print("dumping registry complete...")
                break

    def dump_worker(self, src_path, signal):
        dst_path = self.result_path

        try:
            subprocess.call("RawCopy64.exe /FileNamePath:" + src_path + " /OutputPath:" + dst_path, shell=True)
        except Exception as e:
            print(e)

        signal.put(1)

if __name__ == "__main__":
    result_path = "D:\\Goorm\\Project_2\\code\\Registry"
    user_name = ['yura']
    UTC = 9
    start_time = time.time()
    config = Registry_config("Windows 7", user_name)
    artifact_path = config.run()
    collector = Registry_Collector(result_path, UTC)
    collector.collect(artifact_path)
    end_time = time.time()
    print("complete")
    print("time:", end_time - start_time)