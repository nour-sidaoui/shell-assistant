from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkmacosx import Button

import json
from pynput.keyboard import Key, Controller

import subprocess
import os


keyboard = Controller()


def open_json():
    path = os.path.abspath('config.json')
    subprocess.call(['open', '-a', 'TextEdit', path])


try:
    with open('config.json') as config:
        json_config = json.load(config)
except json.decoder.JSONDecodeError:
    open_json()
    Tk().withdraw()
    messagebox.showerror("invalid config file", "The app couldn't parse the content of config.json.\n"
                                                "Please check if it's JSON valid and try again")
    exit()


def dark_mode_enabled():
    """
        Checks DARK/LIGHT mode of macos.
        return True if DarkMode is active
    """
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    return bool(p.communicate()[0])


def set_min_size():
    """sets root.minsize to the generated window size"""
    root.update()
    w = tab_parent.winfo_reqwidth()
    h = tab_parent.winfo_reqheight() + 33
    root.minsize(w, h)


def launch_open_terminal():
    open_terminal = """osascript -e'
    tell application "Terminal"  
        reopen
        activate
    end tell'
    """
    os.system(open_terminal)


def press_return():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def send_command(cmd_content):
    launch_open_terminal()
    keyboard.type(cmd_content)
    if execute.get() == 1:
        press_return()


def create_all_tabs():
    tab_names_dict = {key: key.split()[0] for key, value in json_config.items()}

    for key, first in tab_names_dict.items():  # key for key name / first for first word using split(' ')
        first = Frame(tab_parent,
                      width=tab_parent.winfo_width(),
                      height=tab_parent.winfo_height(),
                      )

        tab_parent.add(first, text=key)
        x = 0

        for desc, command in json_config[key].items():
            line_frame = LabelFrame(first, bd=0)
            line_frame.pack(side=TOP, fill=X)

            Label(line_frame,
                  width=35,
                  wraplength=300,
                  text=desc,
                  justify=LEFT,
                  anchor=W,
                  padx=10).pack(side=LEFT, fill=X)

            Button(line_frame,
                   text=command,
                   width=350,
                   bg='#4a4a4a' if dark_mode_enabled() else '#dddddd',
                   fg='#dddddd' if dark_mode_enabled() else '#4a4a4a',  # #dddddd = off-white  & #4a4a4a = dark-grey
                   command=lambda p=command: send_command(p)).pack(side=RIGHT, fill=BOTH)

            separator = ttk.Separator(line_frame, orient=HORIZONTAL)
            separator.place(
                relx=0.015,     # starting position on X axis (0.01 == 1% of width)
                rely=0.97,      # starting position on Y axis
                relwidth=0.98,  # width %
                relheight=0.01  # height %
            )

            x += 1
    set_min_size()


if __name__ == '__main__':
    root = Tk()
    root.title('Shell assistant')

    tab_parent = ttk.Notebook(root)
    tab_parent.pack(expand=1, fill='both')

    create_all_tabs()

    customize_frame = LabelFrame(root,
                                 relief=FLAT,
                                 width=tab_parent.winfo_width())
    customize_frame.pack(expand=0, fill='both')
    customize_frame.grid_columnconfigure(3, weight=1)

    Label(customize_frame,
          text=' ',
          # bg='gray92'
          ).grid(row=0, column=0, sticky=W)

    open_json_file = ttk.Button(customize_frame, text="Open JSON file", command=open_json, width=20)
    open_json_file.grid(row=0, column=1, sticky=E)

    open_terminal_button = ttk.Button(customize_frame, text="Open Terminal", command=launch_open_terminal, width=20)
    open_terminal_button.grid(row=0, column=2, sticky=E)

    execute = IntVar()
    execute_check = Checkbutton(customize_frame,
                                text="Execute commands on press",
                                padx=5,
                                pady=5,
                                anchor=W,
                                variable=execute)
    execute_check.grid(row=0, column=3, sticky=E)

    root.mainloop()
