import winreg


class Systeminfo_Collector:
	def __init__(self, result_path):
		self.result_path = result_path
		self.collected_info = {}


	def collect(self):
		current_num = self.get_HKLM_value("SYSTEM\\Select", "Current")
		controlset = "ControlSet00"+str(current_num)

		self.collect_systeminfo(controlset)
		self.collect_accounts()
		self.collect_timezone(controlset)

		self.create_summary()

		return self.collected_info


	def collect_systeminfo(self, controlset):
			self.collected_info["ComputerName"] = self.get_HKLM_value("SYSTEM\\"+controlset+"\\Control\\ComputerName\\ActiveComputerName", "ComputerName")
			self.collected_info["ProductName"] = self.get_HKLM_value("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductName")
			self.collected_info["Processor_Architecture"] = self.get_HKLM_value("SYSTEM\\"+controlset+"\\Control\\Session Manager\\Environment", "Processor_Architecture")
			self.collected_info["InstallPath"] = self.get_HKLM_value("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "SystemRoot")
			self.collected_info["ProductId"] = self.get_HKLM_value("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductId")
			self.collected_info["RegisteredOwner"] = self.get_HKLM_value("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "RegisteredOwner")


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
		handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
		subkey_accounts = winreg.OpenKey(handle, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
		self.collected_info["ProfilePath"] = []
		self.collected_info["AccountName"] = []
		self.collected_info["UserProfile"] = []

		try:
			i = 0
			while True:
				profile_sid = winreg.EnumKey(subkey_accounts, i)
				parts_path = profile_sid.split('-')
				i += 1
				if len(parts_path) < 4 or parts_path[3] != '21':
					continue

				profile_path = self.get_profile_path(profile_sid)
				self.collected_info["ProfilePath"].append(profile_path)

				self.collected_info["AccountName"].append(profile_path.split("\\")[-1])

				account_homepath = self.get_accounts_homepath(account_path)
				self.collected_info["UserProfile"].append(account_homepath)

		except Exception as e:
			pass


	def get_profile_path(self, profile_sid: str) -> str:
		profile_path = self.get_HKLM_value("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\"+profile_sid, "ProfileImagePath")

		os_version = self.collected_info["ProductName"]
		if os_version == "Microsoft Windows XP":
			profile_path = self.collected_info["InstallPath"][0] + profile_path[13:]

		return profile_path


	def get_HKLM_value(self, key_path, subkey_name):
		try:
			subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
			value = winreg.QueryValueEx(subkey, subkey_name)[0]
		except Exception as e:
			print("get value:", e)
			value = ""

		return value


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