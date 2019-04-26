from os import access, R_OK
from os.path import isfile
from sys import exit

class ConfigParser:

	def _load_contents(self, file_path):
		if isfile(file_path) and access(file_path, R_OK):
			with open(file_path, "r", encoding="utf-8") as f:
				return f.read()

	def parse_config(self, config_file):
		contents = self._load_contents(config_file)
		if contents is None:
			print("Can't load config file with path '%s'. Details: file does't exist or no permission to read it" % config_file)
			exit(1)