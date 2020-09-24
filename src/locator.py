from multiprocessing import Process
from include.gui import Window
from numpy import zeros, delete, unravel_index, any as is_not_all_zeros
from texttable import Texttable
from subprocess import call
from re import findall
from tkinter import *
import csv

global resulting_position
class Locator(Process):

	def __init__(self, locator_queue, config, mode):
		super().__init__()
		self.mode = mode
		self._ap_amount = len(config["ap_properties"])
		self._locator_queue = locator_queue
		self._radio_map = self._form_radio_map(config["ap_properties"])
		self.mac_to_name = config["monitoring_properties"]["users"]


	def _form_radio_map(self, ap_properties):
		radio_map = zeros((len(ap_properties), *ap_properties[0]["radio_map"].shape))
		for idx,ap in enumerate(ap_properties):
		    radio_map[idx] = ap["radio_map"]
		return radio_map

	def _form_mac_to_vector_matchings(self, probsup_dumps):
		get_rssi = 0
		mac_to_vector = {mac:zeros(self._radio_map.shape[0]) for mac in self.mac_to_name}
		for idx,probsup_dump in enumerate(probsup_dumps):
			if probsup_dump[0] == 0:
				for mac in mac_to_vector:
					if mac in probsup_dump[1]:
						rssi_tmp = findall(r"%s, state: [0-9]+, cycle: [0-9]+, rssi: (-[0-9]+)" % mac, probsup_dump[1])
						if len(rssi_tmp) > 0:
							mac_to_vector[mac][idx] = int(rssi_tmp[0])
					else:
						mac_to_vector[mac][idx] = 0
			elif probsup_dump[0] == 1:
				for iter in probsup_dump[1]:
					raw_data = iter.split("|")
					if len(raw_data) > 1:
						if raw_data[0].strip() == "hw-addr":
							mac = raw_data[1].strip()
							if mac in self.mac_to_name:
								get_rssi = 1
							else:
								get_rssi = 0
						if raw_data[0].strip() == "rssi-1" and get_rssi == 1:
							rssi_tmp = raw_data[1].strip()
							if len(rssi_tmp) > 0:
								mac_to_vector[mac][idx] = int(rssi_tmp)
								get_rssi = 0
		return mac_to_vector

	def _locate(self, vector):
		if is_not_all_zeros(vector):
			remove_indexes = [idx for idx,rssi in enumerate(vector) if rssi == 0]
			vector = delete(vector, remove_indexes)
			res_indexes = sorted(range(len(vector)), key=lambda i: vector[i], reverse=True)[:3]
			extra_indexes = [i for i, element in enumerate(vector) if i not in res_indexes]
			vector = delete(vector, extra_indexes)
			radio_map = delete(self._radio_map, remove_indexes, axis=0)
			radio_map = delete(radio_map, extra_indexes, axis=0)
			distance_matrix = zeros(radio_map[0].shape)
			for h in range(radio_map[0].shape[0]):
				for v in range(radio_map[0].shape[1]):
					distance_matrix[h,v] = (sum((vector - radio_map[:,h,v]) ** 2)) ** 0.5
			position = unravel_index(distance_matrix.argmin(), distance_matrix.shape)
			return position

	def _data_export(self, mac_to_vector, mac_to_position):
		iter_mac = 0
		iter_rssi = 0
		rssi_fin = [[0.0 for cnt in range (self._ap_amount)] for cnt in range(len(self.mac_to_name))]
		for mac,position in mac_to_position.items():
			iter_rssi = 0
			for rssi in mac_to_vector[mac]:
				if rssi == 0:
					rssi_fin[iter_mac][iter_rssi] = None
				else:
					rssi_fin[iter_mac][iter_rssi] = rssi
				iter_rssi+=1
			iter_mac+=1
		iter_mac = 0
		with open('data/radio_map.csv', 'a+', newline='') as f:
			writer = csv.writer(f)
			for mac,position in mac_to_position.items():
				writer.writerow([mac, self.mac_to_name[mac], rssi_fin[iter_mac]])
				iter_mac += 1

	def _output_positioning_info(self, mac_to_vector, mac_to_position):
		info_table = Texttable()
		info_table.set_cols_align(["c"] * (3 + self._radio_map.shape[0]))
		info_table.set_cols_width([5] * (3 + self._radio_map.shape[0]))
		rows = [["MAC", "Name", "Position"] + ["RSSI from AP%s, dBm" % idx for idx in range(self._radio_map.shape[0])]]
		for mac,position in mac_to_position.items():
		    rows.append([mac, self.mac_to_name[mac], position, *[rssi if rssi != 0 else "N/A" for rssi in mac_to_vector[mac]]])
		info_table.add_rows(rows, header=True)
		call(["clear"])
		print(info_table.draw())

	def run(self):
		# root = Tk()
		# root.geometry("934x312")
		# root.resizable(False, False)
		# app = Window(root)

		while True:
			probsup_dumps = self._locator_queue.get()
			mac_to_vector = self._form_mac_to_vector_matchings(probsup_dumps)
			mac_to_position = {mac:self._locate(vector) for mac,vector in mac_to_vector.items()}

			resulting_position = list(mac_to_position.values())
			# self._data_export(mac_to_vector, mac_to_position)
			self._output_positioning_info(mac_to_vector, mac_to_position)
			# Window.drawPos(app, resulting_position)

			# root.update()
