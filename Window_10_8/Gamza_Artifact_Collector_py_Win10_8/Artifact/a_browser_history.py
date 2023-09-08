import os
from datetime import datetime, timedelta
import shutil
import subprocess
# import time


class Browser_Config:
	def __init__(self, version:str, system_root:str, profile_list:list):
		self.artifact = {}
		self.version = version
		self.system_root = system_root
		self.profile_list = profile_list


	def run(self) -> object:
		self.artifact["Chrome"] = self.get_path_Chrome(self.profile_list, self.version)
		self.artifact["Firefox"] = self.get_path_Firefox(self.profile_list, self.version)
		self.artifact["Edge"] = self.get_path_Edge(self.profile_list, self.version)
		self.artifact["IE"] = self.get_path_IE(self.profile_list, self.version)
		self.artifact["Whale"] = self.get_path_Whale(self.profile_list, self.version)

		return self.artifact


	def get_path_Chrome(self, profile_list, version) -> object:
		collected_path = {}
		default_path = ""

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			collected_path[name+"."+"history"] = []
			collected_path[name+"."+"cache"] = []
			collected_path[name+"."+"cookie"] = []
			collected_path[name+"."+"download"] = []

		if "Windows 10" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 8" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 7" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows XP" in version:
			default_path = "\\Local Settings\\Application Data\\"

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			sub_path = self.get_subpath_Chrome(profile_path+default_path)

			for key in sub_path.keys():
				collected_path[name+"."+key] += sub_path[key]

		return collected_path


	def get_subpath_Chrome(self, path) -> object:
		collected_subpath = {}

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Google" and os.path.isdir(path+item_name):
				path += item_name + "\\"
				break

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Chrome" and os.path.isdir(path+item_name):
				path += item_name + "\\"

				collected_subpath["history"] = [
					path+"User Data\\Default\\History",
					path+"User Data\\Default\\History-journal"
				]
				collected_subpath["cache"] = [
					path+"User Data\\Default\\Cache\\Cache_Data"
				]
				collected_subpath["cookie"] = [
					path+"User Data\\Default\\Cookies",
					path+"User Data\\Default\\Cookies-journal",
					path+"User Data\\Default\\Extension Cookies",
					path+"User Data\\Default\\Extension Cookies-journal"
				]
				collected_subpath["download"] = []

				break

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def get_path_Firefox(self, profile_list, version) -> object:
		collected_path = {}

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			collected_path[name+"."+"history"] = []
			collected_path[name+"."+"cache"] = []
			collected_path[name+"."+"cookie"] = []
			collected_path[name+"."+"download"] = []

		if "Windows 10" in version:
			default_path_local = "\\AppData\\Local\\"
			default_path_roaming = "\\AppData\\Roaming\\"
		elif "Windows 8" in version:
			default_path_local = "\\AppData\\Local\\"
			default_path_roaming = "\\AppData\\Roaming\\"
		elif "Windows 7" in version:
			default_path_local = "\\AppData\\Local\\"
			default_path_roaming = "\\AppData\\Roaming\\"
		elif "Windows XP" in version:
			default_path_local = "\\Local Settings\\Local\\"
			default_path_roaming = "\\AppData\\Roaming\\"

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			sub_path = self.get_subpath_Firefox(profile_path+default_path_local, profile_path+default_path_roaming)

			for key in sub_path.keys():
				collected_path[name+"."+key] += sub_path[key]

		return collected_path


	def get_subpath_Firefox(self, path_local, path_roaming) -> object:
		collected_subpath = {}

		collected_subpath["history"] = []
		collected_subpath["cache"] = []
		collected_subpath["cookie"] = []
		collected_subpath["download"] = []

		dir_list = os.listdir(path_local)
		for item_name in dir_list:
			if item_name == "Mozilla" and os.path.isdir(path_local+item_name):
				path_local += item_name + "\\"
				path_roaming += item_name + "\\"
				break

		dir_list = os.listdir(path_local)
		for item_name in dir_list:
			if item_name == "Firefox" and os.path.isdir(path_local+item_name):
				path_local += item_name + "\\Profiles\\"
				path_roaming += item_name + "\\Profiles\\"
				break

		dir_list = os.listdir(path_local)
		for profile in dir_list:
			sub_path_local = path_local+profile
			sub_path_roaming = path_roaming+profile

			collected_subpath["history"] += [
				sub_path_roaming+"\\places.sqlite"
			]
			collected_subpath["cache"] += [
				sub_path_local+"\\cache2\\doomed",
				sub_path_local+"\\cache2\\entries",
				sub_path_local+"\\cache2\\index",
				sub_path_local+"\\cache2\\index.txt"
			]
			collected_subpath["cookie"] += [
				sub_path_roaming+"\\cookies.sqlite"
			]
			collected_subpath["download"] += [
				sub_path_roaming+"\\download.sqlite"
			]

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def get_path_Edge(self, profile_list, version) -> object:
		collected_path = {}

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			collected_path[name+"."+"history"] = []
			collected_path[name+"."+"cache"] = []
			collected_path[name+"."+"cookie"] = []
			collected_path[name+"."+"download"] = []

		if "Windows 10" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 8" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 7" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows XP" in version:
			return collected_path # not supported

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			sub_path = self.get_subpath_Edge(profile_path+default_path)

			for key in sub_path.keys():
				collected_path[name+"."+key] += sub_path[key]

		return collected_path


	def get_subpath_Edge(self, path) -> object:
		collected_subpath = {}

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Microsoft" and os.path.isdir(path+item_name):
				path += item_name + "\\"
				break

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Edge" and os.path.isdir(path+item_name):
				path += item_name + "\\"

				collected_subpath["history"] = [
					path+"User Data\\Default\\History",
					path+"User Data\\Default\\History-journal"
				]
				collected_subpath["cache"] = [
					path+"User Data\\Default\\Cache\\Cache_Data"
				]
				collected_subpath["cookie"] = [
					path+"User Data\\Default\\Cookies",
					path+"User Data\\Default\\Cookies-journal",
					path+"User Data\\Default\\Extension Cookies",
					path+"User Data\\Default\\Extension Cookies-journal"
				]
				collected_subpath["download"] = []

				break

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def get_path_IE(self, profile_list, version) -> object:
		collected_path = {}

		for profile_path in profile_list:
			name = user.split("\\")[-1]
			collected_path[name+"."+"history"] = []
			collected_path[name+"."+"cache"] = []
			collected_path[name+"."+"cookie"] = []
			collected_path[name+"."+"download"] = []

		if "Windows 10" in version:
			return collected_path # not supported

		elif ("Windows 8" in version) or ("Windows 7" in version):
			default_path_local = "\\AppData\\Local\\Microsoft\\"
			default_path_roaming = "\\AppData\\Roaming\\Microsoft\\"

			for profile_path in profile_list:
				name = profile_path.split("\\")[-1]
				sub_path = self.get_subpath_IE(profile_path+default_path_local, profile_path+default_path_roaming)

				for key in sub_path.keys():
					collected_path[name+"."+key] += sub_path[key]

		elif "Windows XP" in version:
			default_path = "\\Local Settings\\"

			for profile_path in profile_list:
				name = profile_path.split("\\")[-1]
				sub_path = self.get_subpath_IE_XP(profile_path+default_path)

				for key in sub_path.keys():
					collected_path[name+"."+key] += sub_path[key]

		return collected_path


	def get_subpath_IE(self, path_local, path_roaming) -> object:
		collected_subpath = {}

		collected_subpath["history"] = [
			path_local+"Windows\\History\\"
		]
		collected_subpath["cache"] = [
			path_local+"Windows\\Temporary Internet Files\\"
		]
		collected_subpath["cookie"] = [
			path_roaming+"Windows\\Cookies\\"
		]
		collected_subpath["download"] = [
			path_roaming+"Internet Explorer\\DownloadHistory\\"
		]

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def get_subpath_IE_XP(self, path) -> object:
		collected_subpath = {}

		collected_subpath["history"] = [
			path+"History\\"
		]
		collected_subpath["cache"] = [
			path+"Temporary Internet Files\\"
		]
		collected_subpath["cookie"] = [
			path+"Cookies\\"
		]
		collected_subpath["download"] = []

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def get_path_Whale(self, profile_list, version) -> object:
		collected_path = {}

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			collected_path[name+"."+"history"] = []
			collected_path[name+"."+"cache"] = []
			collected_path[name+"."+"cookie"] = []
			collected_path[name+"."+"download"] = []

		if "Windows 10" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 8" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows 7" in version:
			default_path = "\\AppData\\Local\\"
		elif "Windows XP" in version:
			return collected_path # not supported

		for profile_path in profile_list:
			name = profile_path.split("\\")[-1]
			sub_path = self.get_subpath_Whale(profile_path+default_path)

			for key in sub_path.keys():
				collected_path[name+"."+key] += sub_path[key]

		return collected_path


	def get_subpath_Whale(self, path) -> object:
		collected_subpath = {}

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Naver" and os.path.isdir(path+item_name):
				path += item_name + "\\"
				break

		dir_list = os.listdir(path)
		for item_name in dir_list:
			if item_name == "Naver Whale" and os.path.isdir(path+item_name):
				path += item_name + "\\"

				collected_subpath["history"] = [
					path+"User Data\\Default\\History",
					path+"User Data\\Default\\History-journal"
				]
				collected_subpath["cache"] = [
					path+"User Data\\Default\\Cache\\Cache_Data"
				]
				collected_subpath["cookie"] = [
					path+"User Data\\Default\\Cookies",
					path+"User Data\\Default\\Cookies-journal",
					path+"User Data\\Default\\Extension Cookies",
					path+"User Data\\Default\\Extension Cookies-journal"
				]
				collected_subpath["download"] = []

				break

		collected_subpath = self.path_validation_check(collected_subpath)

		return collected_subpath


	def path_validation_check(self, path_object) -> object:
		for key in path_object.keys():
			i = 0
			while i < len(path_object[key]):
				if not os.path.exists(path_object[key][i]):
					del path_object[key][i]
				else:
					i += 1
		return path_object


class Browser_Collector:
	def __init__(self, result_path, UTC):
		self.result_path = result_path
		self.UTC = UTC

		self.collected_info = []


	def collect(self, artifact_path):
		dump_list = self.parse_artifact(artifact_path)
		self.collect_dump(dump_list)
		
		self.create_summary()


	def parse_artifact(self, artifact_path) -> list:
		dump_list = []

		for browser_name in artifact_path.keys():
			browser_path = self.result_path+"\\"+browser_name
			self.mkdir(browser_path)

			browser_artifact = artifact_path[browser_name]
			for artifact_name in browser_artifact.keys():
				if browser_artifact[artifact_name] == []:
					continue

				artifact_subpath = browser_path+"\\"+artifact_name
				self.mkdir(artifact_subpath)
				
				for path in browser_artifact[artifact_name]:
					self.collected_info.append([browser_name] + self.get_file_info(path))
					file_name = path.split("\\")[-1]


					if artifact_name.split(".")[-1] == "cache":
						dump_list.append([path, artifact_subpath+"\\"+file_name])
					else:
						dump_list.append([path, artifact_subpath+"\\"+file_name])

		return dump_list


	def mkdir(self, folder_path):
		try:
			os.mkdir(folder_path)
		except Exception as e:
			print("mkdir:", e)


	def get_file_info(self, file_path) -> list:
		stat = os.stat(file_path)

		name = file_path.split("\\")[-1]
		mtime = self.timestamp_to_UTC(stat.st_mtime)
		atime = self.timestamp_to_UTC(stat.st_atime)
		ctime = self.timestamp_to_UTC(stat.st_ctime)
		size = stat.st_size//1024 # KB

		info = [name, mtime, atime, ctime, size, file_path]
		return info


	def timestamp_to_UTC(self, timestamp) -> datetime:
		utc_offset = timedelta(hours=int(self.UTC))
		utc_modify = datetime.utcfromtimestamp(int(timestamp))+utc_offset

		return utc_modify


	def collect_dump(self, dump_list):
		for dump_path in dump_list:
			self.dump(dump_path[0], dump_path[1])


	def dump(self, src_path, dst_path):
		worker_list = ["doomed", "entries", "index.txt", "index", "data_0", "data_1", "data_2", "data_3"]

		try:
			if os.path.isfile(src_path):
				if src_path.split("\\")[-1] not in worker_list:
					shutil.copy2(src_path, dst_path)
				else:
					self.dump_worker(src_path, "\\".join(dst_path.split("\\")[:-1]))
			else:
				item_list = self.search_directory(src_path, dst_path)

				for item in item_list:
					if item[0].split("\\")[-1] not in worker_list:
						shutil.copy2(item[0], item[1])
					else:
						print(item[0])
						self.dump_worker(item[0], "\\".join(item[1].split("\\")[:-1]))

		except FileNotFoundError:
			print("cannot find the file:", src_path)
	

	def search_directory(self, src_path, dst_path: str) -> list:
		file_list = []

		self.mkdir(dst_path)

		item_list = os.listdir(src_path)
		for item in item_list:
			if os.path.isfile(src_path+"\\"+item):
				file_list.append([src_path+"\\"+item, dst_path+"\\"+item])
			else:
				file_list += self.search_directory(src_path+"\\"+item, dst_path+"\\"+item)

		return file_list
	

	def dump_worker(self, src_path, dst_path):
		try:
			subprocess.run(['RawCopy.exe', '/FileNamePath:'+src_path, '/OutputPath:'+dst_path])

		except subprocess.CalledProcessError as e :
			print("{}: {}".format(e, src_path))


	def create_summary(self):
		output = "EventLog	 UTC+{}\n".format(self.UTC)
		output += "\n\n"

		strFormat = '%-10s%-40s%-25s%-25s%-25s%-20s%s\n'

		title = ['Browser', 'File name', 'Modify time', 'Access time', 'Create time', 'File size(KB)', 'Path']
		output += strFormat %(title[0], title[1], title[2], title[3], title[4], title[5], title[6])

		for info in self.collected_info:
			output += strFormat %(info[0], info[1], info[2], info[3], info[4], info[5], info[6])

		with open(self.result_path+'\\summary.txt', 'w') as f:
			f.write(output)


# if __name__ == "__main__":
# 	result_path = "D:\\Goorm\\Project_2\\code\\Browser"
# 	profile_list = ['C:\\Users\\yura']
# 	UTC = 9
# 	system_root = "C:\\Windows"

# 	start_time = time.time()

# 	config = Browser_Config("Windows 10 Pro", system_root, profile_list)
# 	artifact_path = config.run()

# 	collector = Browser_Collector(result_path, UTC)
# 	collector.collect(artifact_path)

# 	end_time = time.time()

# 	print("complete")
# 	print("time:", end_time-start_time)

# 	end_time = time.time()

# 	print("complete")
# 	print("time:", end_time-start_time)
