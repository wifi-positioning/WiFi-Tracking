from multiprocessing import Process
from numpy import zeros
from re import findall

class Locator(Process):

	def __init__(self, locator_queue, config):
		super().__init__()
		self._locator_queue = locator_queue
		self._radio_map = self._form_radio_map(config["ap_properties"])
		self.mac_to_name = config["monitoring_properties"]["users"]

	def _form_radio_map(self, ap_properties):
		radio_map = zeros((len(ap_properties), *ap_properties[0]["radio_map"].shape))
		for idx,ap in enumerate(ap_properties):
		    radio_map[idx] = ap["radio_map"] 
		return radio_map

	def _form_mac_to_vector_matchings(self, probsup_dumps):
		mac_to_vector = {mac:zeros(self._radio_map.shape[0]) for mac in self.mac_to_name}
		for idx,probsup_dump in enumerate(probsup_dumps):
			for mac in mac_to_vector:
				if mac in probsup_dump:
					rssi = int(findall(r"%s, state: [0-9]+, cycle: [0-9]+, rssi: (-[0-9]+)" % mac, probsup_dump)[0])
					mac_to_vector[mac][idx] = rssi
				else:
					mac_to_vector[mac][idx] = 0
		return mac_to_vector

	def _locate(self, vector):
		pass

	def _output_positioning_info(self, mac_to_vector, mac_to_position):
		print(mac_to_position)

	def run(self):
		while True:
			probsup_dumps = self._locator_queue.get()
			mac_to_vector = self._form_mac_to_vector_matchings(probsup_dumps)
			mac_to_position = {mac:self._locate(vector) for mac,vector in mac_to_vector.items()}
			self._output_positioning_info(mac_to_vector, mac_to_position)	