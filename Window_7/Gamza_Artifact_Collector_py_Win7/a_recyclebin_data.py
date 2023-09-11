# -*- coding: utf-8 -*-
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

    # Check the operating system
    def check_os(self):
        if platform.system() == "Windows":
            self.version = platform.version()
            # print "The current Windows OS version is {}.".format(self.version)
        else:
            print "The current operating system is not Windows."
            sys.exit()

    # Check drives
    def check_drive(self):
        for drive_letter in range(65, 91):
            drive = chr(drive_letter) + ":\\"
            if os.path.exists(drive):
                self.drive_list.append(chr(drive_letter))
        return "Detected drive list:", self.drive_list, "\n"

    # Get the path based on the OS version
    def get_artifact_path(self):
        if "10" in self.version:
            self.artifact_path = ["C", ":\\$Recycle.Bin"]
        elif "8" in self.version:
            self.artifact_path = ["C", ":\\$Recycle.Bin"]
        elif "7" in self.version:
            self.artifact_path = ["C", ":\\$Recycle.Bin"]
        elif "XP" in self.version:
            self.artifact_path = ["C", ":\\Recycler"]
        else:
            print "Unsupported Windows version."
            return None
        return self.artifact_path

    # Create directories
    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError:
                pass

    # Collect artifacts
    def collect(self):
        # Set up collection environment
        self.check_os()
        self.artifact_path = self.get_artifact_path()

        if self.artifact_path is None:
            return  # Exit if the version is not supported

        # Collect artifact information and dump
        # Iterate through drives
        for drive in self.drive_list:
            dir_path = os.path.join(self.result_path, drive)
            self.create_dir(dir_path)

            # Initialize an empty list to write the summary for each drive
            self.recyclebin_info = []
            # Iterate through SIDs
            for root, dirs, files in os.walk(drive + self.artifact_path[1]):
                root_path_list = root.split("\\")
                for dir in dirs:
                    path = ""
                    if (len(root_path_list) - 1) == 1:
                        dir_path = os.path.join(self.result_path, drive, dir)
                    else:
                        path = ""  # Initialize as an empty variable
                        for part in root_path_list[2:]:
                            path += (part + "\\")
                    dir_path = os.path.join(self.result_path, drive, path, dir)
                    self.create_dir(dir_path)
                for file in files:
                    # Dump list
                    src = os.path.join(root, file)
                    path = ""
                    for part in src.split("\\")[2:-1]:
                        path += (part + "\\")
                    dst = os.path.join(self.result_path, drive, path)
                    self.src_dst.append((src, dst))

                    # Get info
                    self.recyclebin_info.append(self.get_file_info(root + "\\" + file))
            self.create_summary(drive)

    def dump(self, src_dst):
        src = src_dst[0]
        dst = src_dst[1]

        try:
            script_dir = os.path.dirname(__file__)
            parent_dir = os.path.join(script_dir)
            rawcopy_path = os.path.join(parent_dir, "RawCopy.exe")
            command = [rawcopy_path, "/FileNamePath:" + src, "/OutputPath:" + dst]
            subprocess.call(command)
        except Exception as e:
            print e
            # shutil.copyfile(src, dst)

    def get_file_info(self, file_path):
        stat = os.stat(file_path)

        name = os.path.basename(file_path)
        mtime = self.timestamp_to_UTC(stat.st_mtime)
        atime = self.timestamp_to_UTC(stat.st_atime)
        ctime = self.timestamp_to_UTC(stat.st_ctime)
        size = stat.st_size  # in bytes

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

        for info in self.recyclebin_info:
            try:
                output += strFormat % (info[0], info[1], info[2], info[3], info[4], info[5])
            except TypeError:
                if self.none_num < len(self.none):
                    output += strFormat % (
                        u"Unable to retrieve file information.", u"", u"", u"", u"", self.none[self.none_num])
                    self.none_num += 1

        with open(os.path.join(self.result_path, drive, 'summary.txt'), 'w') as f:
            f.write(output.encode('utf-8'))

        self.recyclebin_info = []

