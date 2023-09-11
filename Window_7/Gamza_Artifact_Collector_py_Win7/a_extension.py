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

    # Check drives
    def check_drive(self):
        for drive_letter in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return "Detected drive list: {}".format(self.drive_list)

    # Create directories
    def create_dir(self, result_path, drive_list):
        for drive in drive_list:
            for target in self.target_extensions:
                target = target.replace(".", "")
                dir_path = os.path.join(self.result_path, drive, target)
                if not os.path.exists(dir_path):
                    try:
                        os.makedirs(dir_path)
                    except OSError:
                        pass

    # Collect artifact information
    def collect(self):
        # Set up collection environment
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
                except OSError:
                    # Ignore directories with access denied
                    continue

                for item in items:
                    item_path = os.path.join(current_dir, item)
                    if os.path.isdir(item_path):
                        dirs_to_check.append(item_path)
                    elif os.path.isfile(item_path):
                        if os.path.splitext(item)[1] in self.target_extensions:
                            # Dump list
                            target_dir = os.path.splitext(item)[1].replace(".", "")
                            src = item_path
                            dst = os.path.join(self.result_path, drive, target_dir)
                            self.src_dst.append((src, dst))

                            # Get info
                            file_info = self.get_file_info(item_path)
                            if file_info is None:
                                self.none.append(item_path)
                                self.extension_info.append(file_info)
                            else:
                                self.extension_info.append(file_info)

            self.create_summary(drive)

    def dump(self, src_dst):
        src = src_dst[0]
        dst = src_dst[1]

        print(src, dst)
        try:
            script_dir = os.path.dirname(__file__)
            parent_dir = os.path.join(script_dir, "..")
            rawcopy_path = os.path.join(parent_dir, "RawCopy.exe")
            command = [rawcopy_path, "/FileNamePath:" + src, "/OutputPath:" + dst]
            subprocess.call(command)
        except Exception as e:
            print(e)

    def get_file_info(self, file_path):
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            name = file_path.split("\\")[-1]
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
        output = u"Extension     UTC+{}\n".format(self.UTC)  
        for path in self.artifact_path:
            output += path
        output += u"\n\n"

        strFormat = u'%-60s%-25s%-25s%-25s%-20s%s\n'

        title = [u'File name', u'Modify time', u'Access time', u'Create time', u'File size(byte)', u'Path']  
        output += strFormat % (title[0], title[1], title[2], title[3], title[4], title[5])

        for info in self.extension_info:
            try:
                output += strFormat % (info[0], info[1], info[2], info[3], info[4], info[5])
            except TypeError:
                if self.none_num < len(self.none):
                    output += strFormat % (
                        u"Unable to retrieve file information.", u"", u"", u"", u"", self.none[self.none_num])  
                    self.none_num += 1

        with open(os.path.join(self.result_path, drive, 'summary.txt'), 'w') as f:
            f.write(output.encode('utf-8'))  

        self.extension_info = []


