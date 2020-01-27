from argparse import ArgumentParser

class ArgParser:

	def __init__(self):
		self._parser = ArgumentParser()
		self._define_args()

	def _define_args(self):
		self._parser.add_argument("-c", "--config", action="store", type=str,\
		 						  dest="config_file", required=True,\
								  default="data/config.json",\
								  help="Specifying config file, which contains addresses of APs, default is 'data/config.json'.")
		self._parser.add_argument("-m", "--mode", action="store", type=str,\
		 						  dest="mode", required=True,\
								  default="F",\
								  help="Selects the positioning method from exisisting variants: Fingerprinting (F) / Lateration (L).")

	def parse_args(self):
		namespace = self._parser.parse_args()
		return namespace
