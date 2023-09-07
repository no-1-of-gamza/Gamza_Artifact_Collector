import os
from datetime import datetime, timedelta
import shutil


class Registry_config:
    def __init__(self, version:str, user_name:list):
        self.artifact = {}
        self.version = version
        self.user_name = user_name


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
            "C:\\Windows\\SysWOW64\\config",
            "C:\\Users\\Default",
            "C:\\Windows\\ServiceProfiles\\LocalService",
            "C:\\Windows\\ServiceProfiles\\NetworkService"
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Windows\\SysWOW64\\config")
            self.artifact["usrclass"].append("C:\\Windows\\SysWOW64\\config")

        # self.artifact["amcache"] = ["C:\\Windows\\appcompat\\Programs\\Amcache.hive"]


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
            "C:\\Users\\Default",
            "C:\\Windows\\ServiceProfiles\\LocalService",
            "C:\\Windows\\ServiceProfiles\\NetworkService"
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user)
            self.artifact["usrclass"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows")

        # self.artifact["amcache"] = ["C:\\Windows\\AppCompat\\Programs\\Amcache.hive"]


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
            "C:\\Users\\Default",
            "C:\\Windows\\ServiceProfiles\\LocalService",
            "C:\\Windows\\ServiceProfiles\\NetworkService"
        ]
        self.artifact["usrclass"] = []
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user)
            self.artifact["usrclass"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows")


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
            "C:\\Documents and Settings\\Default User",
            "C:\\Documents and Settings\\Administrator",
            "C:\\Documents and Settings\\LocalService",
            "C:\\Documents and Settings\\NetworkService"
        ]
        self.artifact["usrclass"] = [
            "C:\\Documents and Settings\\Administrator\\Local Settings\\Application Data\\Microsoft\\Windows",
            "C:\\Documents and Settings\\LocalService\\Local Settings\\Application Data\\Microsoft\\Windows",
            "C:\\Documents and Settings\\NetworkService\\Local Settings\\Application Data\\Microsoft\\Windows"
        ]
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user)
            self.artifact["usrclass"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows")


class Registry_Collector:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC

        self.collected_info = []


    def collect(self, artifact_path):
        try:
            for path in artifact_path["registry"]:
                self.collected_info.append(self.get_file_info(path))
                # self.collect_dump(path)

            for dir_path in artifact_path["ntuser"]:
                file_list = os.listdir(dir_path)
                for file_name in file_list:
                    if file_name[-10:].upper() == "NTUSER.DAT":
                        self.collected_info.append(self.get_file_info(dir_path+"\\"+file_name))
                        # self.collect_dump(dir_path+"\\"+file_name)

            for dir_path in artifact_path["usrclass"]:
                file_list = os.listdir(dir_path)
                for file_name in file_list:
                    if file_name[-12:].upper() == "USRCLASS.DAT":
                        self.collected_info.append(self.get_file_info(dir_path+"\\"+file_name))
                        # self.collect_dump(dir_path+"\\"+file_name)

        except FileNotFoundError:
            print("FileNotFoundError occur")
        
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
        output = "Registry     UTC+{}\n".format(self.UTC)
        output += "\n\n"

        strFormat = '%-30s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(KB)', 'Path']
        output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.collected_info:
            output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])

        with open(self.result_path+'\\summary.txt', 'w') as f:
            f.write(output)


    def collect_dump(self, file_path):
        try:
            file_name = file_path.split("\\")[-1]
            src_stat = os.stat(file_path)
            dst_file_path = self.result_path+"\\"+file_name

            shutil.copyfile(file_path, dst_file_path)
            os.utime(dst_file_path, (src_stat.st_atime, src_stat.st_mtime))
        except PermissionError:
            print("{}: PermissionError".format(file_path))


#if __name__ == "__main__":
    
    #result_path = ".\\Registry"
    #user_name = ['yura']
    #UTC = 9

    #config = Registry_config("Windows 10 Pro", user_name)
    #artifact_path = config.run()

    #collector = Registry_Collector(result_path, UTC)
    #collector.collect(artifact_path)

    #print("complete")