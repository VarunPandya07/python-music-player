import asyncio
import os
import tkinter as tk
import threading
import pygame
from PIL import ImageTk, Image
from pygame import mixer

PLAY: str = "play"
PAUSE: str = "pause"
RESUME: str = "resume"
END: str = "end"
END_EVENT = 10

song_list: list[str]
last_callback = None
is_stop_pressed = False
current_index: int = 0

song_queue: list[threading.Thread]
active_song: asyncio.Task


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def player_callback(flag: str):
    global PAUSE
    global last_callback

    match flag:
        case "play":
            on_play()

        case "pause":
            on_pause()

        case "resume":
            on_resume()

        case "previous":
            on_previous_song()

        case "next":
            on_next_song()

        case "end":
            print('end callback received.')
            play_next_song()


def init_player():
    global current_index

    play_button.config(state='disabled', command=resume)
    stop_button.config(state='normal')
    pause_button.config(state='normal')

    song = listbox.get(0, tk.ACTIVE)
    running_song.config(text=song)

    asyncio.run_coroutine_threadsafe(play_song(song_list[current_index]), player_loop)


async def play_song(song: str):
    global active_song

    try:

        active_song = asyncio.create_task(start_playing(song))
        player_callback('play')
        await active_song
        player_callback('end')
    except asyncio.CancelledError as err:
        print(f"cancelled song: {song}")
        print(f"cancellation exception: {err.args}")


async def start_playing(song: str):
    mixer.music.set_endevent(END_EVENT)
    mixer.music.load(song)
    mixer.music.play()

    is_playing = True

    while is_playing:
        for event in pygame.event.get():
            if event.type == END_EVENT:
                print('break')
                is_playing = False
        pass


def on_play():
    song = song_list[current_index]

    listbox.select_clear(0, tk.END)
    listbox.selection_set(current_index)
    running_song.config(text=song)


def pause():
    mixer.music.pause()
    player_callback(PAUSE)


def on_pause():
    pause_button.config(state='disabled')
    play_button.config(state='normal')


def resume():
    mixer.music.unpause()
    player_callback(RESUME)


def on_resume():
    pause_button.config(state='normal')
    play_button.config(state='disabled')


def next_song():
    active_song.cancel("play next song requested.")
    player_callback("next")
    mixer.music.stop()
    play_next_song()


def on_next_song():
    pause_button.config(state="normal")
    play_button.config(state="disabled")


def previous_song():
    global current_index

    index = current_index - 1
    if index >= 0:
        active_song.cancel("play previous song requested.")
        current_index = index
        mixer.music.stop()
        asyncio.run_coroutine_threadsafe(play_song(song_list[current_index]), player_loop)
        player_callback("previous")


def on_previous_song():
    if mixer.music.get_busy():
        pause_button.config(state="normal")
        play_button.config(state="disabled")


def play_next_song():
    global current_index
    index = current_index + 1

    if index < len(song_list):
        print('playing new song')
        current_index = index
        asyncio.run_coroutine_threadsafe(play_song(song_list[current_index]), player_loop)


def stop_player():
    global current_index
    # global is_stop_pressed

    # is_stop_pressed = True
    active_song.cancel("stop music player requested.")
    mixer.music.stop()
    play_button.config(command=init_player, state='normal')
    pause_button.config(state='disabled')
    stop_button.config(state='disabled')
    listbox.selection_clear(0, tk.END)
    current_index = 0
    running_song.config(text="choose song.")


def show(songs):
    listbox.selection_clear(0, tk.END)
    for song_name in songs:
        listbox.insert(tk.END, song_name)


co1 = "#ffffff"  # white
co2 = "#3C1DC6"  # purple
co3 = "#333333"  # black
co4 = "#CFC7F8"  # light purple

windows = tk.Tk()
windows.title("")
windows.geometry('352x255')
windows.configure(background=co1)

# frame

lest_frame = tk.Frame(windows, width=150, height=150, bg=co1)
lest_frame.grid(row=0, column=0, padx=1, pady=1)

right_frame = tk.Frame(windows, width=250, height=150, bg=co3)
right_frame.grid(row=0, column=1, padx=0)

down_frame = tk.Frame(windows, width=400, height=100, bg=co4)
down_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=1)

# right frame

listbox = tk.Listbox(right_frame, selectmode=tk.SINGLE, font="Arial 9 bold", width=22, bg=co3, fg=co1)
listbox.grid(row=0, column=0)

w = tk.Scrollbar(right_frame, bg=co1)
w.grid(row=0, column=1)

listbox.configure(yscrollcommand=w.set)
w.config(command=listbox.yview)

# images
img1 = Image.open('icon/1.png')
img1 = img1.resize((130, 130))
img1 = ImageTk.PhotoImage(img1)
app_image = tk.Label(lest_frame, height=130, image=img1, padx=10, bg=co1)
app_image.place(x=15, y=10)


def on_play_button():
    threading.Thread(target=init_player).start()


img2 = Image.open('icon/play button.png')
img2 = img2.resize((30, 30))
img2 = ImageTk.PhotoImage(img2)
play_button = tk.Button(down_frame, width=40, height=50, image=img2, padx=10, bg=co4, font="Ivy 10",
                        command=init_player)

play_button.place(x=58 + 28, y=35)

img3 = Image.open('icon/previous botton.png')
img3 = img3.resize((30, 30))
img3 = ImageTk.PhotoImage(img3)
prev_button = tk.Button(down_frame, width=40, height=50, image=img3, padx=10, bg=co4, font="Ivy 10",
                        command=previous_song)
prev_button.place(x=12 + 28, y=35)

img4 = Image.open('icon/next.png')
img4 = img4.resize((30, 30))
img4 = ImageTk.PhotoImage(img4)
next_button = tk.Button(down_frame, width=40, height=50, image=img4, padx=10, bg=co4, font="Ivy 10",
                        command=next_song)
next_button.place(x=103 + 28, y=35)

img5 = Image.open('icon/pause.png')
img5 = img5.resize((30, 30))
img5 = ImageTk.PhotoImage(img5)
pause_button = tk.Button(down_frame, width=40, height=50, image=img5, padx=10, bg=co4, font="Ivy 10", state='disabled',
                         command=pause)
pause_button.place(x=148 + 28, y=35)

img6 = Image.open('icon/stop-button.png')
img6 = img6.resize((30, 30))
img6 = ImageTk.PhotoImage(img6)
stop_button = tk.Button(down_frame, width=40, height=50, image=img6, padx=10, bg=co4, font="Ivy 10", state='disabled',
                        command=stop_player)
stop_button.place(x=193 + 28, y=35)

img7 = Image.open('icon/fast-forward.png')
img7 = img7.resize((30, 30))
img7 = ImageTk.PhotoImage(img7)
continue_button = tk.Button(down_frame, width=40, height=50, image=img7, padx=10, bg=co4, font="Ivy 10", )
continue_button.place(x=238 + 28, y=35)

running_song = tk.Label(
    down_frame,
    text="choose song",
    font="Ivy 10",
    width=44,
    height=1,
    pady=10,
    bg=co1,
    fg=co3,
    anchor=tk.NW
)
running_song.place(x=0, y=1)

pygame.init()
mixer.init()

player_loop = asyncio.new_event_loop()
player_thread = threading.Thread(target=start_background_loop, args=(player_loop,), daemon=True)
player_thread.start()

os.chdir(r'./m')
song_list = os.listdir()
show(song_list)
music_state = tk.StringVar()
music_state.set("choose one!")

tk.mainloop()
