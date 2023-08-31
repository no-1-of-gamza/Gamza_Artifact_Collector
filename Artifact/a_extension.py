import os
import shutil
from datetime import datetime, timedelta


class Extension:
    def __init__(self, result_path, UTC):
        self.result_path = result_path
        self.UTC = UTC

        self.artifact_path = ["C:\\Users\\ryues\\Downloads\\test"]
        self.target_list = [".txt", ".pdf", ".doc", ".xlsx", ".zip", ".exe", ".lnk"]

        self.extension_info = []

    # 경로를 입력 받을 것인지, 선택할 것인지 고민 (버전 별로 C, D 드라이브 경로는 동일 한 듯)
    def get_artifact_path(self):
        self.artifact_path[0] = input("덤프할 파일 경로를 입력하세요: ")
        print("덤프 파일 경로: ", self.artifact_path)


    def collect(self):
        self.get_artifact_path()

        for path in self.artifact_path:
            file_list = self.get_file_list(path)
            for file_name in file_list:
                if os.path.splitext(file_name)[1] not in self.target_list:
                    continue
                
                # dump
                src = os.path.join(path, file_name)
                dst = os.path.join(self.result_path, file_name)
                shutil.copy2(src, dst)
#                print("파일이 복사되었습니다.")

                # get info
                self.extension_info.append(self.get_file_info(path+"\\"+file_name))
        
        self.create_summary()


    def get_file_list(self, path) -> list:
        dir_list = os.listdir(path)
        file_list = [f for f in dir_list if os.path.isfile(path+'/'+f)]
    
        return file_list


    def get_file_info(self, file_path) -> list:
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
    def create_summary(self):
        output = "Extension     UTC+{}\n".format(self.UTC)
        for path in self.artifact_path:
            output += path+"\n"
        output += "\n\n"

        # 여기서 filename에 해당하는 첫번째 15를 본인 아티팩트에서 나올 수 있는 최대 파일명 길이로 설정
        strFormat = '%-60s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(byte)', 'Path']
        output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.extension_info:
            output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5])

        with open(self.result_path+'\summary.txt', 'w', encoding='utf-8') as f:
            f.write(output)


if __name__ == "__main__":
    result_path = "C:\\Users\\ryues\\Downloads\\Collector\\Extension"
    
    UTC = 9
    artifact = Extension(result_path, UTC)
    artifact.collect()
