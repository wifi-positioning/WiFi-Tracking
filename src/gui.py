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

	def drawFinger(self, position_list):
		self.agent = ImageTk.PhotoImage(Image.open("data/agent.png"))
		self.layer.delete("nmbr")
		for position in position_list:
			if position:
				posX = position[0]
				posY = position[1]
				pixelX = 394 + posX * 28 - 8
				pixelY = 45 + posY * 27 - 13
				self.layer.create_image(pixelX, pixelY, anchor=NW, image=self.agent)
				self.layer.create_text(pixelX+4, pixelY+7, anchor=NW, text=position_list.index(position)+1, tags="nmbr")
				self.layer.pack(fill=BOTH, expand=1)

	def drawLegend(self, clr_arr, coords):
		initCoord = 322
		self.layer.delete("lgnd")
		self.layer.create_rectangle(0, 312, coords[0], coords[1], fill="#FFFFFF", tags="lgnd")
		for iter in range(len(clr_arr)):
			agent = "agent-" + str(iter+1)
			self.layer.create_line(80, initCoord+5+25*iter, 90, initCoord+5+25*iter, fill=clr_arr[iter], width=7, tags="lgnd")
			self.layer.create_text(100, initCoord+25*iter, anchor=NW, font = "Times 14", text=agent, tags="lgnd")
		self.layer.pack(fill=BOTH, expand=1)

	def drawLater(self, distance_list, clr_arr, coords):
		ap_coords = [[140, 240], [500, 180], [880, 220]]
		self.layer.delete("nmbr")
		for agent in range(len(distance_list)):
			if distance_list[agent]:
				for distance in range(len(distance_list[agent])):
					self.layer.create_oval(ap_coords[distance][0] - distance_list[agent][distance] / 0.0383,
										   ap_coords[distance][1] - distance_list[agent][distance] / 0.0383,
										   ap_coords[distance][0] + distance_list[agent][distance] / 0.0383,
										   ap_coords[distance][1] + distance_list[agent][distance] / 0.0383,
										   width=2, outline=clr_arr[agent], tags="nmbr")
					self.layer.pack(fill=BOTH, expand=1)
			self.drawLegend(clr_arr, coords)
