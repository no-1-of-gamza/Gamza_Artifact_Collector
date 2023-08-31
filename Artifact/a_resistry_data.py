import os
from datetime import datetime, timedelta


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
            "C:\\Windows\\SysWOW64\\config\\Default User.NTUSER.DAT",
            "C:\\Windows\\SysWOW64\\config\\Default.NTUSER.DAT",
            "C:\\Users\\Default\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\LocalService\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\NetworkService\\NTUSER.DAT"
        ]
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Windows\\SysWOW64\\config\\"+user+".NTUSER.DAT")
            self.artifact["ntuser"].append("C:\\Windows\\SysWOW64\\config\\"+user+".USRCLASS.DAT")

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
            "C:\\Users\\Default\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\LocalService\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\NetworkService\\NTUSER.DAT"
        ]
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\NTUSER.DAT")
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat")

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
            "C:\\Users\\Default\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\LocalService\\NTUSER.DAT",
            "C:\\Windows\\ServiceProfiles\\NetworkService\\NTUSER.DAT"
        ]
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\NTUSER.DAT")
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat")


    def artifact_WinXP(self):
        self.artifact["registry"] = [
            "C:\\Windows\\system32\\config\\default",
            "C:\\Windows\\system32\\config\\SAM",
            "C:\\Windows\\system32\\config\\SECURITY",
            "C:\\Windows\\system32\\config\\software",
            "C:\\Windows\\system32\\config\\system"
        ]

        self.artifact["ntuser"] = [
            "C:\\WINDOWS\\repair\\ntuser.dat",
            "C:\\Documents and Settings\\Default User\\NTUSER.DAT",
            "C:\\Documents and Settings\\Administrator\\NTUSER.DAT",
            "C:\\Documents and Settings\\LocalService\\NTUSER.DAT",
            "C:\\Documents and Settings\\NetworkService\\NTUSER.DAT"
            "C:\\Documents and Settings\\Administrator\\Local Settings\\Application Data\\Microsoft\\Windows\\UsrClass.dat",
            "C:\\Documents and Settings\\LocalService\\Local Settings\\Application Data\\Microsoft\\Windows\\UsrClass.dat",
            "C:\\Documents and Settings\\NetworkService\\Local Settings\\Application Data\\Microsoft\\Windows\\UsrClass.dat"
        ]
        for user in self.user_name:
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\NTUSER.DAT")
            self.artifact["ntuser"].append("C:\\Users\\"+user+"\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat")


class Registry_Collector:
    def __init__(self, UTC):
        self.result_path = ".\\Registry"
        self.UTC = UTC

        self.collected_info = []


    def collect(self, artifact_path):
        for key in artifact_path.keys():
            for path in artifact_path[key]:
                # get info
                self.collected_info.append(self.get_file_info(path))

                # get dump
                pass
        
        self.create_summary()


    def get_file_info(self, file_path) -> list:
        stat = os.stat(file_path)
        
        name = file_path.split("\\")[-1]
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size//1024 # KB 단위

        info = [name, mtime, atime, ctime, size, file_path]
        return info


    def timestamp_to_UTC(self, timestamp) -> datetime:
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp))+utc_offset

        return utc_modify


    def create_summary(self):
        output = "Registry     UTC+{}\n".format(self.UTC)
        output += "\n\n"

        # 여기서 filename에 해당하는 첫번째 30을 본인 아티팩트에서 나올 수 있는 최대 파일명 길이로 설정
        strFormat = '%-30s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(KB)', 'Path']
        output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.collected_info:
            output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])

        with open(self.result_path+'\\summary.txt', 'w') as f:
            f.write(output)


    def collect_dump(self):
        pass


#if __name__ == "__main__":
    
    #result_path = ".\\Registry"
    #user_name = ['yura']
    #UTC = 9

    #config = Registry_config("Windows 10 Pro", user_name)
    #artifact_path = config.run()

    #collector = Registry_Collector(result_path, UTC)
    #collector.collect(artifact_path)

    #print("complete")