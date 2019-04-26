from argparse import ArgumentParser

class ArgParser:

	def __init__(self):
		self._parser = ArgumentParser()  
		self._define_args()

	def _define_args(self):
		self._parser.add_argument("-c", action="store", type=str, dest="config_file", required=True)

	def parse_args(self):
		namespace = self._parser.parse_args()
		return namespace.config_file

