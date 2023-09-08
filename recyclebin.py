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

        self.src = []
        self.dst = []

        self.none = []
        self.none_num = 0

    # 운영체제 확인
    def check_os(self):
        if platform.system() == "Windows":
            self.version = platform.version()
            #print(f"현재 사용 중인 Windows 운영체제 버전은 {self.version} 입니다.")
        else:
            print("현재 사용 중인 운영체제는 Windows가 아닙니다.")
            sys.exit()

    # 드라이브 확인
    def check_drive(self):
        for drive_letter  in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return print("확인된 드라이브 목록:", self.drive_list, "\n")
    
    # 버전 별, 아티팩트 경로
    def get_artifact_path(self):
        if "10" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "8" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "7" in self.version:
            self.artifact_path = ["C", ":\$Recycle.Bin"]
        elif "XP" in self.version:
            self.artifact_path = ["C", ":\Recycler"]
        else:
            print("지원되지 않는 Windows 버전입니다.")
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
        # 수집 환경 세팅
        self.check_os()
        self.artifact_path = self.get_artifact_path()

        if self.artifact_path is None:
            return  # 지원되지 않는 버전이면 종료
        
        # 아티팩트 정보 수집 및 덤프
        # 드라이브 별로 반복
        for drive in self.drive_list:
            dir_path = os.path.join(self.result_path, drive)
            self.create_dir(dir_path)

            # 드라이브 별로 summary를 작성하기 위해 빈 리스트로 초기화
            self.recyclebin_info = []
            # sid 별로 반복
            for root, dirs, files in os.walk(drive+self.artifact_path[1]):
                root_path_list = root.split("\\")
                for dir in dirs:
                    path = ""
                    if (len(root_path_list)-1) == 1:
                        dir_path = os.path.join(self.result_path, drive, dir)
                    else:
                        path = ""   # 빈 변수로 초기화
                        for part in root_path_list[2:]:
                            path += (part + "\\")
                    dir_path = os.path.join(self.result_path, drive, path, dir)
                    self.create_dir(dir_path)
                for file in files:
                    # dump list
                    src = os.path.join(root, file)
                    self.src.append(src)
                    path = ""
                    for part in src.split("\\")[2:-1]:
                        path += (part + "\\")
                    dst = os.path.join(self.result_path, drive, path)
                    self.dst.append(dst)
                    #print("src: "+src+"\ndst: "+dst+"\n")
                    
                    # get info
                    self.recyclebin_info.append(self.get_file_info(root+"\\"+file))
            self.create_summary(drive)

    def dump(self):
        if len(self.src) != len(self.dst):
            print("다름")
        for src, dst in zip(self.src, self.dst):
            try: 
                shutil.copyfile(src, dst)
            except OSError:
                # 권한 오류가 난다면 해당 프로그램 사용
                subprocess.run([r"C:\Users\ryues\OneDrive\바탕 화면\RawCopy.exe", "/FileNamePath:"+src, "/OutputPath:"+dst])

    def get_file_info(self, file_path):
        stat = os.stat(file_path)

        name = os.path.basename(file_path)
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size  # byte 단위

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
                    output += strFormat %("파일 정보를 가져올 수 없습니다.", "", "", "", "", self.none[self.none_num])
#                    print("none 처리 완료")
                    self.none_num += 1

        with open(os.path.join(self.result_path, drive, 'summary.txt'), 'w', encoding='utf-8') as f:
            f.write(output)

if __name__ == "__main__":
    result_path = "C:\\Users\\ryues\\Downloads\\Collector\\RecycleBin"
    UTC = 9

    artifact = RecycleBin(result_path, UTC)
    artifact.check_drive()

    artifact.collect()

    pool = multiprocessing.Pool(processes=4)
    pool.apply_async(artifact.dump)
    print("완료")
    pool.close()
    pool.join()