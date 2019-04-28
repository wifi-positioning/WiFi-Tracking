from multiprocessing.dummy import Pool
from time import sleep

class Engine:

	def __init__(self, config):
		self.ap_list = config["ap_properties"]
		self.poll_interval = config["monitoring_properties"]["poll_interval"]
		self._thread_pool = Pool(len(config["ap_properties"]))

	def _fetch_probsup_dump(self, ap):
		return ap["ip_address"]

	def run(self):
		while True:
			results = self._thread_pool.map(self._fetch_probsup_dump, self.ap_list)
			print(results)
			sleep(self.poll_interval)