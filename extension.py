import os
import shutil
import subprocess
import multiprocessing
from datetime import datetime, timedelta


class Extension:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC

        self.drive_list = []
        self.artifact_path = []
        self.target_list = [".txt", ".pdf", ".doc", ".xlsx", ".zip", ".exe", ".lnk"]

        self.extension_info = []

        self.src = []
        self.dst = []
        
        self.none = []
        self.none_num = 0

    # 드라이브 확인
    def check_drive(self):
        for drive_letter  in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return print("확인된 드라이브 목록:", self.drive_list, "\n")

    # 폴더 생성
    def create_dir(self, result_path, drive_list):
        for drive in drive_list:
            for target in self.target_list:
                target = target.replace(".", "")
                dir_path = os.path.join(self.result_path, drive, target)
                if not os.path.exists(dir_path):
                    try:
                        os.makedirs(dir_path)
                    except FileExistsError:
                        pass
    
    # 아티팩트 정보 수집
    def collect(self):
        # 수집 환경 세팅
        file_list = []
        self.check_drive()
        self.create_dir(self.result_path, self.drive_list)

        for drive in self.drive_list:
            self.artifact_path = os.path.join(drive + ':\\')
            for root, _, files in os.walk(self.artifact_path):
                file_list.append(files)
                for file_name in files:
                    if os.path.splitext(file_name)[1] not in self.target_list:
                        continue
                
                    # dump list
                    target_dir = os.path.splitext(file_name)[1].replace(".", "")
                    src = os.path.join(root, file_name)
                    dst = os.path.join(self.result_path, drive, target_dir)
                    self.src.append(src)
                    self.dst.append(dst)
                    #print("src: "+src+"\ndst: "+dst+"\n")

                    # get info
                    file_info = self.get_file_info(root+"\\"+file_name)
                    if file_info is None:
                        self.none.append(root+"\\"+file_name)
                        self.extension_info.append(file_info)
                        #print(root+"\\"+file_name)
                        #print(self.get_file_info(root+"\\"+file_name))
                    else:
                        self.extension_info.append(file_info)

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

    def get_file_info(self, file_path) -> list:
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
        
            name = file_path.split("\\")[-1]
            mtime = self.timestamp_to_UTC(stat.st_mtime)
            atime = self.timestamp_to_UTC(stat.st_atime)
            ctime = self.timestamp_to_UTC(stat.st_ctime)
            size = stat.st_size # byte 단위

            info = [name, mtime, atime, ctime, size, file_path]

            return info


    def timestamp_to_UTC(self, timestamp) -> datetime:
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp))+utc_offset

        return utc_modify

    # summary.txt
    def create_summary(self, drive):
        output = "Extension     UTC+{}\n".format(self.UTC)
        for path in self.artifact_path:
            output += path
        output += "\n\n"

        # 여기서 filename에 해당하는 첫번째 15를 본인 아티팩트에서 나올 수 있는 최대 파일명 길이로 설정
        strFormat = '%-60s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(byte)', 'Path']
        output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.extension_info:
            try:
                output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])
            except TypeError:
                if self.none_num < len(self.none):
                    output += strFormat %("파일 정보를 가져올 수 없습니다.", "", "", "", "", self.none[self.none_num])
                    #print("none 처리 완료")
                    self.none_num += 1
        
        with open(self.result_path+'\\'+drive+'\summary.txt', 'w', encoding='utf-8') as f:
            f.write(output)
        
        self.extension_info = []


if __name__ == "__main__":
    # 감자 아티팩트 수집 도구 경로
    result_path = "C:\\Users\\ryues\\Downloads\\Collector\\Extension"
    
    UTC = 9

    artifact = Extension(result_path, UTC)
    artifact.create_dir(result_path, artifact.drive_list)
    artifact.collect()

    pool = multiprocessing.Pool(processes=4)
    pool.apply_async(artifact.dump)
    pool.close()
    pool.join()
