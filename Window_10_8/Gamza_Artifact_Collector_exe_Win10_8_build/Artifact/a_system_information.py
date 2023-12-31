import winreg


class Systeminfo_Collector:
	def __init__(self, result_path):
		self.result_path = result_path
		self.collected_info = {}


	def collect(self):

		subkey_select = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\Select", 0, winreg.KEY_READ)
		controlset = "ControlSet00"+str(winreg.QueryValueEx(subkey_select, "Current")[0])

		self.collect_systeminfo(controlset)
		self.collect_accounts()
		self.collect_timezone(controlset)

		self.create_summary()

		return self.collected_info


	def collect_systeminfo(self, controlset):

		subkey_computername = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\"+controlset+"\\Control\\ComputerName\\ActiveComputerName", 0, winreg.KEY_READ)
		self.collected_info["ComputerName"] = winreg.QueryValueEx(subkey_computername, "ComputerName")[0]

		subkey_osname = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
		self.collected_info["ProductName"] = winreg.QueryValueEx(subkey_osname, "ProductName")[0]

		subkey_architecture = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\"+controlset+"\\Control\\Session Manager\\Environment", 0, winreg.KEY_READ)
		self.collected_info["Processor_Architecture"] = winreg.QueryValueEx(subkey_architecture, "PROCESSOR_ARCHITECTURE")[0]

		subkey_installpath = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
		self.collected_info["InstallPath"] = winreg.QueryValueEx(subkey_installpath, "SystemRoot")[0]

		subkey_productid = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
		self.collected_info["ProductId"] = winreg.QueryValueEx(subkey_productid, "ProductId")[0]

		subkey_owner = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ)
		self.collected_info["RegisteredOwner"] = winreg.QueryValueEx(subkey_owner, "RegisteredOwner")[0]


	def collect_timezone(self, controlset):
		subkey_timezone = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\"+controlset+"\\Control\\TimeZoneInformation", 0, winreg.KEY_READ)
		timezone_key = winreg.QueryValueEx(subkey_timezone, "TimeZoneKeyName")[0]
		timezone_utc = 0

		# more timezone: https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones?view=windows-11
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

		self.collected_info["Timezone"] = timezone_utc


	def collect_accounts(self):
		handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
		subkey_accounts = winreg.OpenKey(handle, "")
		self.collected_info["AccountName"] = []
		self.collected_info["UserProfile"] = []

		try:
			i = 0
			while True:
				account_path = winreg.EnumKey(subkey_accounts, i)
				parts_path = account_path.split('-')
				i += 1
				if len(parts_path) < 4 or parts_path[3] != '21':
					continue

				account_name = self.get_accounts_name(account_path)
				self.collected_info["AccountName"].append(account_name)

				account_homepath = self.get_accounts_homepath(account_path)
				self.collected_info["UserProfile"].append(account_homepath)

		except Exception as e:
			pass


	def get_accounts_name(self, account_path) -> str:
		handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
		subkey_accounts = winreg.OpenKey(handle, account_path+"\\Volatile Environment")
		account_name = ""

		win_version = self.collected_info["ProductName"]
		if win_version == "Microsoft Windows XP":
			res = winreg.QueryValueEx(subkey_accounts, "HOMEPATH")[0]
			account_name = res.split("\\")[-1]
		else:
			account_name = winreg.QueryValueEx(subkey_accounts, "USERNAME")[0]

		return account_name


	def get_accounts_homepath(self, account_path) -> str:
		handle = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
		subkey_accounts = winreg.OpenKey(handle, account_path+"\\Volatile Environment")

		win_version = self.collected_info["ProductName"]
		if win_version == "Microsoft Windows XP":
			account_name = winreg.QueryValueEx(subkey_accounts, "HOMEPATH")[0]
		else:
			account_name = winreg.QueryValueEx(subkey_accounts, "USERPROFILE")[0]

		return account_name


	def create_summary(self):
		output = "System Info\n"
		output += "\n\n"

		strFormat = '%-30s%s\n'

		title = ['Type', 'Content']
		output += strFormat %(title[0], title[1])

		for key in self.collected_info.keys():
			if type(self.collected_info[key]) == list:
				list_result = ""
				for item in self.collected_info[key]:
					list_result += item+"\t"
				output += strFormat %(key, list_result)

			else:
				output += strFormat %(key, self.collected_info[key])

		with open(self.result_path+'\\summary.txt', 'w') as f:
			f.write(output)


if __name__ == "__main__":
	result_path = ".\\SystemInfo"

	collector = Systeminfo_Collector(result_path)
	system_info = collector.collect()

	# print("complete")