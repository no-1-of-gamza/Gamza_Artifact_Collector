import wmi
import os

import ctypes

def list_physical_disks():
    c = wmi.WMI()
    physical_disks = c.Win32_DiskDrive()
    disk_list = []
    for disk in physical_disks:
        disk_list.append(disk.DeviceID)
    return disk_list

if __name__ == "__main__":
    physical_disks = list_physical_disks()
    if not physical_disks:
        print("사용 가능한 물리 디스크가 없습니다.")
    else:
        print("사용 가능한 물리 디스크 목록:")
        for disk in physical_disks:
            print(disk)
            extend_path = disk + "\\$Extend"
