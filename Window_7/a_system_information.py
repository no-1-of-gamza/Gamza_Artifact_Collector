# -*- coding: utf-8 -*-
import _winreg as winreg

class Systeminfo_Collector:
    def __init__(self, result_path):
        self.result_path = result_path
        self.collected_info = {}

    def collect(self):
        subkey_select = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\Select", 0, winreg.KEY_READ)
        controlset = "ControlSet00" + str(winreg.QueryValueEx(subkey_select, "Current")[0])

        self.collect_systeminfo(controlset)
        self.collect_accounts()
        self.collect_timezone(controlset)

        self.create_summary()

        return self.collected_info

    def collect_systeminfo(self, controlset):
        subkey_computername = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\" + controlset + "\\Control\\ComputerName\\ActiveComputerName", 0, winreg.KEY_READ)
        self.collected_info[u"ComputerName"] = winreg.QueryValueEx(subkey_computername, "ComputerName")[0]

        subkey_osname = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
        self.collected_info[u"ProductName"] = winreg.QueryValueEx(subkey_osname, "ProductName")[0]

        subkey_architecture = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\" + controlset + "\\Control\\Session Manager\\Environment", 0, winreg.KEY_READ)
        self.collected_info[u"Processor_Architecture"] = winreg.QueryValueEx(subkey_architecture, "PROCESSOR_ARCHITECTURE")[0]

        subkey_installpath = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
        self.collected_info[u"InstallPath"] = winreg.QueryValueEx(subkey_installpath, "SystemRoot")[0]

        subkey_productid = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
        self.collected_info[u"ProductId"] = winreg.QueryValueEx(subkey_productid, "ProductId")[0]

        subkey_owner = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
        self.collected_info[u"RegisteredOwner"] = winreg.QueryValueEx(subkey_owner, "RegisteredOwner")[0]

    def collect_timezone(self, controlset):
        subkey_timezone = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\" + controlset + "\\Control\\TimeZoneInformation", 0, winreg.KEY_READ)
        timezone_key = winreg.QueryValueEx(subkey_timezone, "TimeZoneKeyName")[0]
        timezone_utc = 0

        if timezone_key == "West Pacific Standard Time" or timezone_key == "AUS Eastern Standard Time":
            timezone_utc = 10
        elif timezone_key == "Korea Standard Time" or timezone_key == "Tokyo Standard Time":
            timezone_utc = 9
        elif timezone_key == "China Standard Time" or timezone_key == "Singapore Standard Time" or timezone_key == "Taipei Standard Time":
            timezone_utc = 8
        elif timezone_key == "Pacific Standard Time":
            timezone_utc = -8
        elif timezone_key == "Eastern Standard Time":
            timezone_utc = -5
        elif timezone_key == "GMT Standard Time":
            timezone_utc = 0

        self.collected_info[u"Timezone"] = timezone_utc

    def collect_accounts(self):
        handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
        subkey_accounts = winreg.OpenKey(handle, "")
        self.collected_info[u"AccountName"] = []
        self.collected_info[u"UserProfile"] = []

        try:
            i = 0
            while True:
                account_path = winreg.EnumKey(subkey_accounts, i)
                parts_path = account_path.split('-')
                i += 1 
                if len(parts_path) < 4 or parts_path[3] != '21':
                    continue

                account_name = self.get_accounts_name(account_path)
                self.collected_info[u"AccountName"].append(account_name)

                account_homepath = self.get_accounts_homepath(account_path)
                self.collected_info[u"UserProfile"].append(account_homepath)

        except Exception as e:
            pass

    def get_accounts_name(self, account_path):
        handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
        subkey_accounts = winreg.OpenKey(handle, account_path + "\\Volatile Environment")
        account_name = ""

        win_version = self.collected_info[u"ProductName"]
        if win_version == "Microsoft Windows XP":
            res = winreg.QueryValueEx(subkey_accounts, "HOMEPATH")[0]
            account_name = res.split("\\")[-1]
        else:
            account_name = winreg.QueryValueEx(subkey_accounts, "USERNAME")[0]

        return account_name
    
    def get_accounts_homepath(self, account_path):
        handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
        subkey_accounts = winreg.OpenKey(handle, account_path + "\\Volatile Environment")

        win_version = self.collected_info["ProductName"]
        if win_version == "Microsoft Windows XP":
            account_name = winreg.QueryValueEx(subkey_accounts, "HOMEPATH")[0].encode('utf-8')
        else:
            account_name = winreg.QueryValueEx(subkey_accounts, "USERPROFILE")[0].encode('utf-8')

        return account_name

    def create_summary(self):
        output = u"System Info\n"
        output += u"\n\n"

        strFormat = u'%-30s%s\n'

        title = [u'Type', u'Content']
        output += strFormat % (title[0], title[1])

        for key in self.collected_info.keys():
            if type(self.collected_info[key]) == list:
                list_result = u""
                for item in self.collected_info[key]:
                    list_result += item + u"\t"
                output += strFormat % (key, list_result)

            else:
                output += strFormat % (key, self.collected_info[key])

        with open(self.result_path + u'\\summary.txt', 'w') as f:
            f.write(output.encode('utf-8'))

if __name__ == "__main__":
    result_path = u".\\SystemInfo"  # 결과 경로도 유니코드 문자열로 변경

    collector = Systeminfo_Collector(result_path)
    system_info = collector.collect()  # 이 system_info가 메인으로 넘어가면 됨
