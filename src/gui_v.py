#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.master = master
		self.initUI()

	def initUI(self):
		self.master.title("WiFi Positioning")
		self.pack(fill=BOTH, expand=1)
		self.map = ImageTk.PhotoImage(Image.open("data/map.png"))
		self.layer = Canvas(self, width=934, height=312)
		self.layer.create_image(0, 0, anchor=NW, image=self.map)
		self.layer.pack(fill=BOTH, expand=1)


# 1 px = 3.83 cm = 0.0383 m - That's important
	def drawPos(self, distance_list):
		ap_coords = [[140, 240], [500, 180], [880, 220]]
		tst_colors = ["#FF00FF","#000000","#FFFF00","#00FFFF","#FF0F0F"]
		agent_nmbr = 0
		self.layer.delete("nmbr")
		for agent in distance_list:
			if agent:
				ap_nmbr = 0
				for distance in agent:
					tst = self.layer.create_oval(ap_coords[ap_nmbr][0] - distance/0.0383, ap_coords[ap_nmbr][1] - distance/0.0383,
										   ap_coords[ap_nmbr][0] + distance/0.0383, ap_coords[ap_nmbr][1] + distance/0.0383,
										   width=2, outline=tst_colors[agent_nmbr], tags="nmbr")
					self.layer.pack(fill=BOTH, expand=1)
					ap_nmbr =+ 1
			agent_nmbr =+ 1
