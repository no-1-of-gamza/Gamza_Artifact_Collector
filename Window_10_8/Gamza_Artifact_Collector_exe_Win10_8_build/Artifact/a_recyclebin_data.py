import os
import sys
import shutil
import platform
import subprocess
import multiprocessing
from datetime import datetime, timedelta

class RecycleBin:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC

        self.artifact_path = []

        self.version = []
        self.user_sid_list = []
        self.drive_list = []

        self.recyclebin_info = []

        self.src_dst = []

        self.none = []
        self.none_num = 0

    # 운영체제 확인
    def check_os(self):
        if platform.system() == "Windows":
            self.version = platform.version()
        else:
            print("The operating system you are currently using is not Windows.")
            sys.exit()

    # 드라이브 확인
    def check_drive(self):
        for drive_letter  in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return print("Drives:", self.drive_list, "\n")
    
    # 버전 별, 아티팩트 경로
    def get_artifact_path(self):
        if "10" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "8" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "8.1" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "6.3" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "7" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "XP" in self.version:
            self.artifact_path = ["C", ":\Recycler"]
        else:
            print("Unsupported version of Windows.")
            print(self.version)
            return None
        return self.artifact_path

    # 폴더 생성
    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except FileExistsError:
                pass

    # 아티팩트 수집
    def collect(self):
        self.check_os()
        self.artifact_path = self.get_artifact_path()

        if self.artifact_path is None:
            return 
        
  
        for drive in self.drive_list:
            dir_path = os.path.join(self.result_path, drive)
            self.create_dir(dir_path)

            self.recyclebin_info = []
            for root, dirs, files in os.walk(drive+self.artifact_path[1]):
                root_path_list = root.split("\\")
                for dir in dirs:
                    path = ""
                    if (len(root_path_list)-1) == 1:
                        dir_path = os.path.join(self.result_path, drive, dir)
                    else:
                        path = ""  
                        for part in root_path_list[2:]:
                            path += (part + "\\")
                    dir_path = os.path.join(self.result_path, drive, path, dir)
                    self.create_dir(dir_path)
                for file in files:
                    # dump list
                    src = os.path.join(root, file)
                    path = ""
                    for part in src.split("\\")[2:-1]:
                        path += (part + "\\")
                    dst = os.path.join(self.result_path, drive, path)
                    self.src_dst.append((src, dst))
                    #print("src: "+src+"\ndst: "+dst+"\n")
                    
                    # get info
                    self.recyclebin_info.append(self.get_file_info(root+"\\"+file))
            self.create_summary(drive)

    def dump(self, src_dst_tuple):
        src, dst = src_dst_tuple
        try:          
            subprocess.run(["RawCopy.exe", "/FileNamePath:"+src, "/OutputPath:"+dst])
        except OSError:
            shutil.copyfile(src, dst)

    def get_file_info(self, file_path):
        stat = os.stat(file_path)

        name = os.path.basename(file_path)
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size 

        info = [name, mtime, atime, ctime, size, file_path]
        return info

    def timestamp_to_UTC(self, timestamp):
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp)) + utc_offset
        return utc_modify

    def create_summary(self, drive):
        output = "RecycleBin     UTC+{}\n".format(self.UTC)
        output += self.artifact_path[0] + "\n\n"

        strFormat = '%-60s%-25s%-25s%-25s%-20s%s\n'
        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(byte)', 'Path']
        output += strFormat % (title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.recyclebin_info:
            try:
                output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])
            except TypeError:
                if self.none_num < len(self.none):
                    output += strFormat %("Unable to get file information.", "", "", "", "", self.none[self.none_num])
                    #print("none 처리 완료")
                    self.none_num += 1

        with open(os.path.join(self.result_path, drive, 'summary.txt'), 'w', encoding='utf-8') as f:
            f.write(output)

