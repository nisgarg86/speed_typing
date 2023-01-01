import typing
import json
import random

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from utils import (create_new_window,
                   calculate_avg_inaccurate_char_per_word,
                   get_background_color,
                   update_timer,
                   create_time_taken_string,
                   calculate_words_per_minute)


def start(config: typing.Dict):

    window = create_new_window(config)

    # adding image
    frame = ttk.Frame(window, width=config['window-width'], height=config['window-height'])
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open("speed_typing.jpeg"))

    # Create a Label Widget to display the text or Image
    label = ttk.Label(frame, image=img)
    label.pack()

    start_button = ttk.Button(window, text='START', command=lambda: create_instructions_window(config, window))
    start_button.pack()
    start_button.place(anchor='center', relx=0.5, rely=0.8)

    window.mainloop()


def create_instructions_window(config: typing.Dict, prev_window: tk.Tk):

    prev_window.destroy()

    window = create_new_window(config)
    instruction_list = config['instructions']

    text = tk.Text(window, width=config['window-width'], height=5)

    for idx, sentence in enumerate(instruction_list):
        text.insert('end', '\u2022 ')
        text.insert('end', sentence)
        text.insert('end', '\n')

    text.configure(state='disabled')
    text.pack()

    start_button = ttk.Button(window, text='START TEST', command=lambda: create_game_window(config, window))
    start_button.pack()
    start_button.place(anchor='center', relx=0.5, rely=0.8)

    window.attributes('-topmost', 1)
    window.mainloop()


def create_game_window(config: typing.Dict, prev_window: tk.Tk):

    prev_window.destroy()

    window = create_new_window(config)

    # choosing random text
    file_num = random.randint(1, 5)

    with open(f'typing_text/text_{file_num}.txt') as f:
        text = f.read()

    # timer label
    timer = ttk.Label(text='00:00:00')
    timer.pack()
    # timer.place(anchor='center', relx=0.5, rely=0.1)

    # target label
    # target_label = ttk.Label(text='Text to Type')
    # target_label.pack()
    # target_label.place(anchor='center', relx=0.5, rely=0.3)

    # target text
    text_box = tk.Text(window, width=config['window-width'], height=12)
    text_box.insert('end', text)
    text_box.configure(state='disabled')
    text_box.pack()
    # text_box.place(anchor='center', relx=0.5, rely=0.2)

    # target label
    # type_label = ttk.Label(text='Type Your Text Here')
    # type_label.pack()
    # type_label.place(anchor='center', relx=0.5, rely=0.5)

    # input box
    type_box = tk.Text(window, width=config['window-width'], height=12)
    type_box.pack()
    # type_box.place(anchor='center', relx=0.5, rely=0.3)

    # submit button
    start_button = ttk.Button(window, text='SUBMIT TEST', command=lambda: submit_text(config,
                                                                                      window,
                                                                                      type_box,
                                                                                      text_box,
                                                                                      timer))
    start_button.pack()
    start_button.place(anchor='center', relx=0.5, rely=0.9)

    # updating timer
    window.after(1000, update_timer, timer, window)
    window.mainloop()


def submit_text(config: typing.Dict, prev_window: tk.Tk, type_box: tk.Text, text_box: tk.Text, timer: ttk.Label):

    #####################################################
    ############## Calculating Statistics ###############
    #####################################################

    # calculating text accuracy
    output_text = type_box.get('1.0', 'end')
    input_text = text_box.get('1.0', 'end')
    avg_inaccurate_char_per_word = calculate_avg_inaccurate_char_per_word(output_text, input_text)
    bg_color = get_background_color(avg_inaccurate_char_per_word)

    # calculating time taken
    time_string = timer.cget('text')
    time_parts = time_string.split(':')
    hours, minutes, seconds = time_parts[0], time_parts[1], time_parts[2]
    time_taken_string = create_time_taken_string(hours, minutes, seconds)

    # calculating wpm
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    wpm = calculate_words_per_minute(len(output_text.split(' ')), total_seconds)
    wpm_bg = get_background_color(wpm)

    prev_window.destroy()
    window = create_new_window(config)

    score_label = ttk.Label(text=f'Average incorrect characters per word = {avg_inaccurate_char_per_word}',
                            foreground=bg_color)
    score_label.pack()
    score_label.place(anchor='center', relx=0.5, rely=0.4)

    time_label = ttk.Label(text=time_taken_string)
    time_label.pack()
    time_label.place(anchor='center', relx=0.5, rely=0.5)

    wpm_label = ttk.Label(text=f'Words per minute - {wpm}', foreground=wpm_bg)
    wpm_label.pack()
    wpm_label.place(anchor='center', relx=0.5, rely=0.6)

    window.mainloop()


if __name__ == '__main__':

    with open('config.json') as _file:
        app_config = json.load(_file)

    start(app_config)
