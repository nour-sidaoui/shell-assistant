from tkinter import *
from tkinter import ttk
from subprocess import call
import json
import os

with open('config.json') as config:
    json_config = json.load(config)


def open_json():
    path = os.path.abspath('config.json')
    call(['open', '-a', 'TextEdit', path])


def set_min_size():
    """sets root.minsize to the generated window size"""
    root.update()
    w = tab_parent.winfo_reqwidth()
    h = tab_parent.winfo_reqheight() + 33
    root.minsize(w, h)


def launch_terminal():
    open_terminal = """osascript -e 'tell application "Terminal" to activate'"""
    os.system(open_terminal)


def press_return():
    press_enter = """osascript -e 'tell application "System Events" to keystroke return'
    """
    os.system(press_enter)


def send_command(cmd_content):
    com1 = """osascript -e'
    tell application "Terminal"
        activate
    end tell
    tell application "System Events"
        set textToType to """ + '"' + str(cmd_content) + '"' + """
        delay 1
        keystroke textToType
    end tell'
    """
    os.system(com1)

    if execute.get() == 1:
        press_return()


def create_all_tabs():
    tab_names_dict = {key: key.split()[0] for key, value in json_config.items()}

    for key, first in tab_names_dict.items():  # key for key name / first for first word using split(' ')
        first = Frame(tab_parent,
                      width=tab_parent.winfo_width(),
                      height=tab_parent.winfo_height(),
                      bg='gray92')

        tab_parent.add(first, text=key)
        x = 0

        for desc, command in json_config[key].items():
            line_frame = LabelFrame(first, bd=1)
            line_frame.pack(side=TOP, fill=X)

            Label(line_frame,
                  width=35,
                  wraplength=300,
                  bg='white',
                  text=desc,
                  justify=LEFT,
                  anchor=W,
                  padx=10).pack(side=LEFT, fill=X)

            Button(line_frame,
                   text=command,
                   width=35,
                   bd=0,
                   command=lambda p=command: send_command(p)).pack(side=RIGHT, fill=BOTH)
            x += 1
    set_min_size()


if __name__ == '__main__':
    root = Tk()
    root.title('Shell assistant')

    tab_parent = ttk.Notebook(root)
    tab_parent.pack(expand=1, fill='both')

    create_all_tabs()

    customize_frame = LabelFrame(root,
                                 bg='gray92',
                                 relief=SUNKEN,
                                 width=tab_parent.winfo_width())
    customize_frame.pack(expand=0, fill='both')
    customize_frame.grid_columnconfigure(3, weight=1)

    Label(customize_frame, text=' ', bg='gray92').grid(row=0, column=0, sticky=W)

    open_json_file = ttk.Button(customize_frame, text="Open JSON file", command=open_json, width=20)
    open_json_file.grid(row=0, column=1, sticky=E)

    open_terminal_button = ttk.Button(customize_frame, text="Launch Terminal", command=launch_terminal, width=20)
    open_terminal_button.grid(row=0, column=2, sticky=E)

    execute = IntVar()
    execute_check = Checkbutton(customize_frame,
                                text="Execute commands on press",
                                bg='gray92',
                                padx=5,
                                pady=5,
                                anchor=W,
                                variable=execute)
    execute_check.grid(row=0, column=3, sticky=E)

    root.mainloop()
