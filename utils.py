import typing

import tkinter as tk
from tkinter import ttk
import Levenshtein


def create_new_window(config: typing.Dict) -> tk.Tk:

    window = tk.Tk()
    window.title('Game Window')

    window_width = config['window-width']
    window_height = config['window-height']
    margix_x, margin_y = get_window_margins(window, window_width, window_height, config['window-centered'])

    window.geometry(f'{window_width}x{window_height}+{margix_x}+{margin_y}')

    if not config['window-resizable']:
        window.resizable(False, False)
    else:
        window.resizable(None, None)

    return window


def get_window_margins(window: tk.Tk,
                       window_width: float,
                       window_height: float,
                       window_centered: bool) -> typing.Tuple[float, float]:

    if not window_centered:
        return 100, 100

    screen_width, screen_height = get_screen_dimensions(window)

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    return center_x, center_y


def get_screen_dimensions(window: tk.Tk) -> typing.Tuple[float, float]:

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    return screen_width, screen_height


def calculate_avg_inaccurate_char_per_word(text_1: str, text_2: str) -> float:

    text_1_word_list = text_1.split(' ')
    text_2_word_list = text_2.split(' ')

    total_lv_distance = 0

    for i in range(max(len(text_1_word_list), len(text_2_word_list))):
        word_1 = text_1_word_list[i] if i < len(text_1_word_list) else ''
        word_2 = text_2_word_list[i] if i < len(text_2_word_list) else ''

        lv_distance = Levenshtein.distance(word_1, word_2)
        total_lv_distance += lv_distance

    avg_inaccurate_char_per_word = total_lv_distance / max(len(text_2_word_list), len(text_1_word_list))

    return round(avg_inaccurate_char_per_word, 2)


def get_background_color(score: float):

    if score <= 2:
        return 'green'
    elif 2 < score <= 3.5:
        return 'yellow'
    else:
        return 'red'


def update_timer(timer_label: ttk.Label, window: tk.Tk):

    label_string = timer_label.cget('text')
    next_time_string = get_next_time(label_string)
    timer_label.config(text=next_time_string)
    window.after(1000, update_timer, timer_label, window)


def get_next_time(time_string: str) -> str:

    time_parts = list(map(int, time_string.split(':')))
    hours, minutes, seconds = time_parts[0], time_parts[1], time_parts[2]

    seconds += 1

    if seconds == 60:
        seconds = 0
        minutes += 1

    if minutes == 60:
        minutes = 0
        hours += 1

    seconds = str(seconds).zfill(2)
    minutes = str(minutes).zfill(2)
    hours = str(hours).zfill(2)

    return ':'.join([hours, minutes, seconds])


def create_time_taken_string(hours: str, minutes: str, seconds: str) -> str:

    string_builder = ['Total time taken -']

    if int(hours) > 0:
        string_builder.append(f'{hours} hours')
    if int(minutes) > 0:
        string_builder.append(f'{minutes} minutes')
    if int(seconds) > 0:
        string_builder.append(f'{seconds} seconds')

    return ' '.join(string_builder)


def calculate_words_per_minute(word_count: int, time_in_seconds: int) -> float:

    if time_in_seconds > 0:
        return round(word_count / time_in_seconds, 2)
    return 0
