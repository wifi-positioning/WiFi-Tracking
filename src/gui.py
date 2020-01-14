#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("WiFi Positioning")
        self.pack(fill=BOTH, expand=1)

        self.map = ImageTk.PhotoImage(Image.open("data/map.png"))

        canvas = Canvas(self, width=724, height=242)
        canvas.create_image(0, 0, anchor=NW, image=self.map)
        canvas.pack(fill=BOTH, expand=1)

    def drawPos(position):
        print(position)

    def main():
        root = Tk()
        app = Window(root)
        root.mainloop()

if __name__ == '__main__':
    main()
