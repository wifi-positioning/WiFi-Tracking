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

    def drawPos(self, position):
        posX = position[0][0]
        posY = position[0][1]

# pixelX = Top left angle of the blue box on map + N Square * Grid Multiply - Half of the phone's img size
# pixelY = Top left angle of the blue box on map + N Square * Grid Multiply - Half of the phone's img size
        pixelX = 394 + posX * 28 - 8
        pixelY = 45 + posY * 27 - 13
        print("Relative coordinates:\n X: ", posX, "Y: ", posY)
        print("Pixel coordinates:\n X: ", pixelX, "Y: ", pixelY)
        print()

        self.agent = ImageTk.PhotoImage(Image.open("data/agent.png"))
        self.layer.create_image(pixelX, pixelY, anchor=NW, image=self.agent)
        self.layer.pack(fill=BOTH, expand=1)
