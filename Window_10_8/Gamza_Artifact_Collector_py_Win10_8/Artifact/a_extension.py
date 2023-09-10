# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import multiprocessing
from datetime import datetime, timedelta
import argparse

class Extension:
    def __init__(self, result_path, UTC, target_extensions):
        self.result_path = result_path
        self.UTC = UTC
        self.target_extensions = target_extensions

        self.drive_list = []
        self.artifact_path = []
        self.extension_info = []
        self.src_dst = []
        self.none = []
        self.none_num = 0

    # 드라이브 확인
    def check_drive(self):
        for drive_letter in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return print("확인된 드라이브 목록:", self.drive_list, "\n")

    # 폴더 생성
    def create_dir(self, result_path, drive_list):
        for drive in drive_list:
            for target in self.target_extensions:
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
            dirs_to_check = [self.artifact_path]

            while dirs_to_check:
                current_dir = dirs_to_check.pop()
                try:
                    items = os.listdir(current_dir)
                except PermissionError as e:
                    # 액세스 거부된 디렉토리인 경우 무시
                    continue

                for item in items:
                    item_path = os.path.join(current_dir, item)
                    if os.path.isdir(item_path):
                        dirs_to_check.append(item_path)
                    elif os.path.isfile(item_path):
                        if os.path.splitext(item)[1] in self.target_extensions:
                            # dump list
                            target_dir = os.path.splitext(item)[1].replace(".", "")
                            src = item_path
                            dst = os.path.join(self.result_path, drive, target_dir)
                            self.src_dst.append((src, dst))

                            # get info
                            file_info = self.get_file_info(item_path)
                            if file_info is None:
                                self.none.append(item_path)
                                self.extension_info.append(file_info)
                            else:
                                self.extension_info.append(file_info)

            self.create_summary(drive)

    def dump(self, src_dst_tuple):
        if len(self.src) != len(self.dst):
            print("len is different")
        src, dst = src_dst_tuple
            try:
                shutil.copyfile(src, dst)
            except OSError:
                script_dir = os.path.dirname(__file__)
                parent_dir = os.path.join(script_dir, "..")
                rawcopy_path = os.path.join(parent_dir, "RawCopy.exe")
                command = [rawcopy_path, "/FileNamePath:" + src, "/OutputPath:" + dst]
                subprocess.run(command)

    def get_file_info(self, file_path) -> list:
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            name = file_path.split("\\")[-1]
            mtime = self.timestamp_to_UTC(stat.st_mtime)
            atime = self.timestamp_to_UTC(stat.st_atime)
            ctime = self.timestamp_to_UTC(stat.st_ctime)
            size = stat.st_size

            info = [name, mtime, atime, ctime, size, file_path]
            return info

    def timestamp_to_UTC(self, timestamp) -> datetime:
        utc_offset = timedelta(hours=int(self.UTC))
        utc_modify = datetime.utcfromtimestamp(int(timestamp)) + utc_offset
        return utc_modify

    def create_summary(self, drive):
        output = "Extension     UTC+{}\n".format(self.UTC)
        for path in self.artifact_path:
            output += path
        output += "\n\n"

        strFormat = '%-60s%-25s%-25s%-25s%-20s%s\n'

        title = ['File name', 'Modify time', 'Access time', 'Create time', 'File size(byte)', 'Path']
        output += strFormat % (title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.extension_info:
            try:
                output += strFormat % (info[0], info[1], info[2], info[3], info[4], info[5])
            except TypeError:
                if self.none_num < len(self.none):
                    output += strFormat % (
                        "파일 정보를 가져올 수 없습니다.", "", "", "", "", self.none[self.none_num])
                    self.none_num += 1

        with open(self.result_path + '\\' + drive + '\summary.txt', 'w', encoding='utf-8') as f:
            f.write(output)

        self.extension_info = []

def main():
    result_path = "C:\\Users\\ryues\\Downloads\\Collector\\Extension"
    UTC = 9

    parser = argparse.ArgumentParser(description="Artifact Collector")
    parser.add_argument("--extensions", nargs="+", default=[".txt", ".pdf", ".doc", ".xlsx", ".zip", ".exe", ".lnk"],
                        help="List of extensions to collect")
    args = parser.parse_args()

    artifact = Extension(result_path, UTC, args.extensions)
    artifact.create_dir(result_path, artifact.drive_list)
    artifact.collect()

    with multiprocessing.Pool(processes=4) as pool:
        pool.map(artifact.dump, artifact.src_dst)

    print("완료")

if __name__ == "__main__":
    main()
