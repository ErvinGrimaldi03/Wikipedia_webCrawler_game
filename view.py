import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os
import crawler_end

def _sendDetector(impulso):
    print(impulso)

class ROOT:
    def __init__(self, root):
        global view
        view = root
        self.root = root

        self.root.geometry("720x1080")
        self.background_color = "self.root['bg']="
        self.text_color = "black"
        ROOT.run(self)


    def register_button(self):
        parola = self.start_lable.get()
        print(parola)

    def run(self):
        self.start_lable = tk.Entry(
            self.root,
            text = "Starting page",
            textvariable = tk.StringVar
        )

        self.sent_button = tk.Button(
            text="SEND",
            command=lambda x=None: self.register_button()
        )



        self.start_lable.pack()
        self.sent_button.pack()
        self.root.mainloop()



    def _set_bgc(self, new_color):
        exec(f"{self.background_color}'{new_color}'")
        self.sent_button["bg"]= "white"

    def _set_txtColor(self, new_color):
        self.text_color = new_color


if __name__ == "__main__":
    _startup = tk.Tk()
    start = ROOT(_startup)