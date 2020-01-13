#!/usr/bin/env python3
from tkinter import *

class Window(Frame):
    def __init__(self, resulting_position):
        Frame.__init__(self, resulting_position)
        self._position = resulting_position
        self.init_UI()

    def init_UI(self):
        self.pack(fill=BOTH, expand=1)
        self.draw_table()

    def draw_table(self):
        table = Canvas(root, width=1000, height=600, bg='white')
        table.pack()
        print(self._position)
        tst="tst"
        tst_x=500
        tst_y=150
        table.create_text(tst_x, tst_y, text=tst,
            justify=CENTER, font="Verdana 14")
        table.create_rectangle(100, 50, 900, 250)


root = Tk()
root.title("WiFi Positioning")
root.geometry("1000x600")
root.resizable(False, False)
app = Window(root)
root.mainloop()
