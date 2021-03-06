import os, time, threading, getpass
from mutagen.mp3 import MP3
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from ttkthemes import themed_tk as themetk
from pygame import mixer
from tinytag import TinyTag
from PyLyrics import *

# GUI creation
root_var = themetk.ThemedTk()  # Setting the the theme

root_var.get_themes()  # Retrieving the available themes from themed_tk
root_var.set_theme("breeze")  # Setting the breeze theme to the UI

root_var.title("MP3 Player")  # Program name (title on GUI)
root_var.iconbitmap(r"Icons/music_note.ico")  # Setting an icon & it's location
root_var.resizable(False, False)  # Users are locked from altering the GUI size

"""
Major components of the 'root_var' are STATUS_BAR, FIRST_FRAME, SECOND_FRAME, THIRD_FRAME
    *FIRST_FRAME -> # something
    *SECOND_FRAME -> TOP_FRAME, MIDDLE_FRAME, BOTTOM_FRAME
    *THIRD_FRAME -> PlayList 
"""

# Status Bar
username = getpass.getuser()  # We use the getpass module to get the name of the current user
status_bar = ttk.Label(root_var, text="Welcome Christopher", anchor=SW)
# status_bar = ttk.Label(root_var, text="Welcome " + username, anchor=SW)
status_bar.pack(side=BOTTOM, fill=X)

mixer.init()  # Initializing the mixer module

# Menu Bar
menu_bar = Menu(root_var)  # Initializing an empty menu bar
root_var.config(menu=menu_bar)


# Defining a function to browse and select a file from the user's desktop
def select_file():
    global filename
    index = 0
    filename = filedialog.askopenfilenames()
    if filename is not "":
        for file_path in filename:
            exact_filename = os.path.basename(file_path)  # Exact filename without the path
            playlist_box.insert(index, exact_filename)  # Adding the file to the playlist in the GUI
            playlist_array.insert(index, file_path)  # Adding the file path to the playlist array
            index += 1
    else:
        print("Did not select a file when user went to browse!")


# Defining a function to delete files from the playlist box
def del_file():
    selected_song = playlist_box.curselection()
    selected_song = int(selected_song[0])  # Selecting the index from selected_song
    playlist_box.delete(selected_song)
    playlist_array.pop(selected_song)


# A fn to clear the user's song history log
def clear_history():
    clear_file = r"History/Song History.txt"
    with open(clear_file, "r+") as file:
        file.seek(0)
        file.truncate()
        file.write("## SONGS HISTORY LOG\n")
        file.write("\n")
        file.seek(22)


# Sub Menu Bar
sub_menu = Menu(menu_bar, tearoff=0)  # Initializing a sub menu (no#1)
menu_bar.add_cascade(label="File", menu=sub_menu)  # Creating a bar with the name 'File', and it has a sub menu
sub_menu.add_command(label="Open", command=select_file)  # Creating a sub menu with the name 'Open'
sub_menu.add_command(label="Clear History", command=clear_history)  # Creating a sub menu to clear song history log
sub_menu.add_command(label="Exit", command=root_var.destroy)  # Creating a sub menu with the name 'Exit'


# Defining a fn to display the following message on clicking About from Help
def about_us():
    messagebox.showinfo("About MP3 Player", '''MP3 Player is a simple audio player, that was developed as a learning project.
    
    Created By:- Christopher J.S.
    
    If you wish to make a contribution to this software, email me at christo77793@gmail.com''')


def lyrics_help():
    messagebox.showinfo("Lyrics FAQ", '''I used the PyLyrics module to display lyrics.
    
    Website:- https://lyrics.fandom.com/wiki/LyricWiki
    
    If no lyrics are shown despite the spelling being correct, look up for the song and artist name from the above website and try again.''')


# Sub Menu Bar
sub_menu = Menu(menu_bar, tearoff=0)  # Initializing a sub menu (no#2)
menu_bar.add_cascade(label="Help", menu=sub_menu)  # Creating a bar with the name 'Help', and it has a sub menu
sub_menu.add_command(label="About", command=about_us)  # Creating a sub menu with the name 'About'
sub_menu.add_command(label="Lyrics", command=lyrics_help)  # Creating a sub menu with the name 'Lyrics'

# Creating frames to improve design of the GUI
# first_frame
# second_frame
# third_frame

first_frame = ttk.Frame(root_var)  # First Frame
first_frame.pack(side=LEFT, padx=15)

# Creating the lyric box

lyrics_option_frame = ttk.Frame(first_frame)  # Creating a separate frame to store user interactive options
lyrics_option_frame.pack(side=BOTTOM)

singer_name = ttk.Label(lyrics_option_frame, text="Artist Name:")  # A label for the singer's name
singer_name.grid(row=0, column=0, pady=15, padx=15)

singer_name_input = ttk.Entry(lyrics_option_frame, background="lightgray")  # An entry to get singer's name
singer_name_input.grid(row=0, column=1, pady=15, padx=15)

singer_song = ttk.Label(lyrics_option_frame, text="Song Name:")  # A label for the singer's song's name
singer_song.grid(row=1, column=0, padx=15)

singer_song_input = ttk.Entry(lyrics_option_frame, background="lightgray")  # An entry to get singer's song's name
singer_song_input.grid(row=1, column=1, padx=15)

song_lyrics = "Please be connected to the internet to view lyrics!"


def show_lyrics():
    global song_lyrics
    artist_name = singer_name_input.get()
    artist_song = singer_song_input.get()

    if song_lyrics is not "":
        song_lyrics = ""
        lyric_box.config(state=NORMAL)
        lyric_box.delete(1.0, END)
        lyric_box.config(state=DISABLED)

    try:
        song_lyrics = PyLyrics.getLyrics(artist_name, artist_song)
        status_bar["text"] = "Lyrics found!"
    except ValueError:
        song_lyrics = "Please be connected to the internet to view lyrics!"
        status_bar["text"] = "Lyrics not found, recheck spelling!"

    lyric_box.config(state=NORMAL)
    lyric_box.insert(END, song_lyrics)
    lyric_box.config(state=DISABLED)  # Users cannot edit textbox


search = ttk.Button(lyrics_option_frame, text="Search Lyrics", command=show_lyrics)  # A button to show lyrics
search.grid(row=2, column=0, pady=25)


def remove_lyrics():
    global song_lyrics
    song_lyrics = "Please be connected to the internet to view lyrics!"
    lyric_box.config(state=NORMAL)
    lyric_box.delete(1.0, END)
    lyric_box.insert(END, song_lyrics)
    lyric_box.config(state=DISABLED)  # Users cannot edit textbox
    status_bar["text"] = "Lyrics removed!"


remove = ttk.Button(lyrics_option_frame, text="Remove Lyrics", command=remove_lyrics)  # A button to remove lyrics
remove.grid(row=2, column=1, pady=25)

lyric_label = ttk.Label(first_frame, text="Enter the name of a song and it's artist to see it's lyrics")
lyric_label.pack(pady=15, padx=5)

lyric_box_scrollbar = ttk.Scrollbar(first_frame, orient=VERTICAL)
lyric_box = Text(first_frame, height=15, width=39, background="lightgray", bd=0, yscrollcommand=lyric_box_scrollbar.set)
lyric_box_scrollbar.config(command=lyric_box.yview)
lyric_box_scrollbar.pack(side=RIGHT, fill=Y)
lyric_box.pack(pady=25, padx=5)

lyric_box.config(state=NORMAL)
lyric_box.insert(END, song_lyrics)
lyric_box.config(state=DISABLED)  # Users cannot edit textbox


third_frame = ttk.Frame(root_var)  # Third Frame
third_frame.pack(side=RIGHT, padx=15)

# Creating a playlist

playlist_frame = ttk.Frame(third_frame)  # A frame for the playlist box and it's dependencies
playlist_frame.pack(side=TOP)


playlist_array = []

playlist_box_scrollbar = ttk.Scrollbar(playlist_frame, orient=VERTICAL)  # Creating a scrollbar for the playlist
playlist_box = Listbox(playlist_frame, height=13, width=39, bd=0, background="lightgray", yscrollcommand=playlist_box_scrollbar.set)
playlist_box_scrollbar.config(command=playlist_box.yview)  # Configuring the scrollbar
playlist_box_scrollbar.pack(side=RIGHT, fill=Y)
playlist_box.pack(pady=15, padx=5)


playlist_option_frame = ttk.Frame(third_frame)  # A frame for the playlist box and it's dependencies
playlist_option_frame.pack(padx=15)

playlist_label = ttk.Label(playlist_option_frame, text="Your playlist")
playlist_label.grid(row=0, column=1, pady=5, padx=15)

add_song_icon = PhotoImage(file=r"Images/add_song.png")  # Adding an icon for the add songs button
add_song_btn = ttk.Button(playlist_option_frame, image=add_song_icon, command=select_file)  # A button to add songs to the list
add_song_btn.grid(row=1, column=0, pady=15, padx=5)

del_song_icon = PhotoImage(file=r"Images/del_song.png")  # Adding an icon for the delete songs button
del_song_btn = ttk.Button(playlist_option_frame, image=del_song_icon, command=del_file)  # A button to delete songs from the list
del_song_btn.grid(row=1, column=2, pady=15, padx=5)


# Defining a fn to repeat songs
change_repeat_song_icon = False  # a variable to change repeat icon
check_var = False  # a variable to break the while loop


def rep_song():
    global change_repeat_song_icon, check_var
    if not change_repeat_song_icon:
        rep_song_btn.configure(image=rep_song_on_icon)
        change_repeat_song_icon = True
        check_var = True
    else:
        rep_song_btn.configure(image=rep_song_off_icon)
        change_repeat_song_icon = False
        check_var = False
    t2 = threading.Thread(target=check_rep)  # Running an isolated thread to loop music
    t2.start()


def check_rep():  # A function to loop music and reverse it
    while check_var:  # loop to continuously play music repeatedly
        if mixer.music.get_busy():
            pass
        else:
            loop_song()
        if not check_var:
            get_audio_time = get_time()
            unloop_song(get_audio_time)
            break


allow_repeat = False


def loop_song():
    global allow_repeat
    if allow_repeat:
        play_button(-1)
    else:
        pass


def get_time():
    selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
    selected_song = int(selected_song[0])  # Converts tuple to int
    to_play = playlist_array[selected_song]  # Provides the file path from the playlist array

    file_extension = os.path.splitext(to_play)

    if file_extension[1] == ".mp3":
        sound_file = MP3(to_play)
        file_time_span = sound_file.info.length
    else:
        sound_file = mixer.Sound(to_play)
        file_time_span = sound_file.get_length()

    total_length = file_time_span

    currently_at = mixer.music.get_pos()
    currently_at /= 1000
    currently_at = int(currently_at)

    remaining_time = total_length - currently_at
    remaining_time = int(remaining_time)

    return remaining_time


def unloop_song(get_audio_time):
    global allow_repeat
    time.sleep(get_audio_time)
    stop_button()
    allow_repeat = False


# Repeat button
rep_song_off_icon = PhotoImage(file=r"Images/repeat_off.png")  # Adding an icon for the repeat song button
rep_song_on_icon = PhotoImage(file=r"Images/repeat_on.png")  # Adding an icon for the repeat song button
rep_song_btn = ttk.Button(playlist_option_frame, image=rep_song_off_icon, command=rep_song)  # A button to delete songs from the list
rep_song_btn.grid(row=1, column=1, pady=15, padx=5)


second_frame = ttk.Frame(root_var)  # Second Frame
second_frame.pack(padx=15)


top_frame = ttk.Frame(second_frame)  # Second Top Frame
top_frame.pack(pady=25)

# Audio file details

last_played_song = ttk.Label(top_frame, text="Add a song to start listening to some music")  # Displays audio length in the play fn
last_played_song.pack(pady=15)

audio_times = ttk.Label(top_frame, text="")  # Displays the current time of the audio
audio_times.pack()


middle_frame = ttk.Frame(second_frame)  # Second Middle Frame
middle_frame.pack(padx=25, pady=25)


# Defining a function to display audio details
def audio_details():
    try:
        global file_time_span

        current_time = mixer.music.get_pos() / 1000  # Getting the current position of the song

        selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
        selected_song = int(selected_song[0])  # Converts tuple to int
        to_play = playlist_array[selected_song]  # Provides the file path from the playlist array

        file_extension = os.path.splitext(to_play)

        if file_extension[1] == ".mp3":
            sound_file = MP3(to_play)
            file_time_span = sound_file.info.length
        else:
            sound_file = mixer.Sound(to_play)
            file_time_span = sound_file.get_length()

        total_time = time.strftime("%H:%M:%S", time.gmtime(file_time_span))  # Converting the total time to a time format

        current_time += 1

        if int(song_slider.get()) == int(file_time_span):
            last_played_song["text"] = "Last played song:- " + os.path.basename(to_play)
            audio_times["text"] = ""

        elif int(song_slider.get()) == int(current_time):  # Song slider has not been moved

            song_slider.config(to=int(file_time_span), value=int(current_time))  # Adjusting the slider position as the song furthers
            converted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))  # Converting it to a time format
            audio_times["text"] = f"Time elapsed:- {converted_current_time} of {total_time}"

        else:  # Song slider has been moved

            song_slider.config(to=int(file_time_span), value=int(song_slider.get()))  # Adjusting the slider position as the song furthers
            converted_current_time = time.strftime("%H:%M:%S", time.gmtime(int(song_slider.get())))  # Converting it to a time format
            audio_times["text"] = f"Time elapsed:- {converted_current_time} of {total_time}"

            temp_var = int(song_slider.get()) + 1  # Incrementing the slider as we move along
            song_slider.config(value=temp_var)

        if mixer.music.get_busy():
            audio_times.after(1000, audio_details)  # Calling the fn every one second
        else:
            audio_times["text"] = ""

    except NameError:
        print("No song is being played to move the song position!")


# Defining a button to play music
song_heard = 0


def play_button(repeat):
    global to_un_pause, paused, check_val, allow_repeat, to_play, song_heard, file_time_span
    if to_un_pause:
        mixer.music.unpause()  # Resumes the music from when it was paused
        to_un_pause = False

        selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
        selected_song = int(selected_song[0])  # Converts tuple to int
        to_play = playlist_array[selected_song]  # Provides the file path from the playlist array

        song_metadata = TinyTag.get(to_play)
        bitrate = song_metadata.bitrate
        song_offset = song_metadata.audio_offset

        if song_heard > 1:
            status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset) + " | You have heard this song " + str(song_heard) + " times"
        else:
            status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset)
    else:
        try:
            mixer.music.stop()

            selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
            selected_song = int(selected_song[0])  # Converts tuple to int
            to_play = playlist_array[selected_song]  # Provides the file path from the playlist array

            mixer.music.load(to_play)
            mixer.music.play(repeat)

            song_metadata = TinyTag.get(to_play)
            bitrate = song_metadata.bitrate
            song_offset = song_metadata.audio_offset
            audio_details()

            check_val = True
            paused = True
            allow_repeat = True


            song_heard = song_counter()
            if song_heard > 1:
                status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset) + " | You have heard this song " + str(song_heard) + " times"
            else:
                status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset)

            last_played_song["text"] = ""

        except Exception:
            # Since no file has been selected the following code will be executed
            messagebox.showwarning("Warning", "No file has been selected to play!")


# Play button
play_icon = PhotoImage(file=r"Images/play-button.png")  # Adding an icon for the play button
play_btn = ttk.Button(middle_frame, image=play_icon, command=lambda: play_button(0))  # Adding the play button
play_btn.grid(row=0, column=0, pady=25, padx=15)


# Defining a button to pause music
to_un_pause = False
paused = False


def pause_button():
    global to_un_pause
    to_un_pause = True
    mixer.music.pause()
    status_bar["text"] = "Music paused!"  # Setting the status as paused
    if not paused:
        # Code to handle the case, in which the user intentionally or not pauses first without playing any music
        status_bar["text"] = "No music is being played to pause!"


# Pause button
pause_icon = PhotoImage(file=r"Images/pause-button.png")  # Adding an icon for the pause button
pause_btn = ttk.Button(middle_frame, image=pause_icon, command=pause_button)  # Adding the play button
pause_btn.grid(row=0, column=1, pady=25, padx=15)


# Defining a button to stop music
check_val = False


def stop_button():
    global check_val, allow_repeat
    if check_val:
        mixer.music.stop()
        status_bar["text"] = "Music stopped!"  # Setting the status as stopped
        last_played_song["text"] = "Last played song:- " + os.path.basename(to_play)
        audio_times["text"] = ""

        allow_repeat = False

        song_slider.config(value=0)  # Setting the slider to the beginning when a song is stopped
    else:
        # Setting the status to show nothing is being played if user hits stop when no music is being played
        status_bar["text"] = "No music is being played to stop!"


# Stop button
stop_icon = PhotoImage(file=r"Images/stop-button.png")  # Adding an icon for the stop button
stop_btn = ttk.Button(middle_frame, image=stop_icon, command=stop_button)  # Adding the stop button
stop_btn.grid(row=0, column=2, pady=25, padx=15)


slider_frame = ttk.Frame(second_frame)  # Creating a seperate frame for the song slider
slider_frame.pack()


# Defining a scale to slide song
def slide_song(x):
    try:
        global file_time_span

        selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
        selected_song = int(selected_song[0])  # Converts tuple to int
        to_play = playlist_array[selected_song]  # Provides the file path from the playlist array

        mixer.music.load(to_play)
        mixer.music.play(loops=0, start=int(song_slider.get()))

    except IndexError:
        print("No song is being played to move the song position!")


# Song slider
song_slider = ttk.Scale(slider_frame, from_=0, to_=100, value=0, orient=HORIZONTAL, command=slide_song, length=310)
song_slider.pack()


# Function to list number of times a song was heard {displays only if the count is > 1}
def song_counter():
    repeated_count = 0  # A variable to get the count of the no of times the user has heard a song
    count_file = r"History/Song History.txt"
    with open(count_file, "r+") as file:
        content = file.read()
        exact_file_name = os.path.basename(to_play)
        if exact_file_name in content:
            repeated_count = content.count(exact_file_name)
            file.write(exact_file_name + "\n")
        else:
            file.write(exact_file_name + "\n")
    return repeated_count


bottom_frame = ttk.Frame(second_frame)  # Second Bottom Frame
bottom_frame.pack(padx=25, pady=25)


# Defining a button to mute/un-mute
muted = False
present_vol = mixer.music.get_volume()


def mute_music():
    global muted
    if not muted:
        mixer.music.set_volume(0)
        volume_btn.configure(image=mute_icon)
        muted = True
    else:
        global present_vol
        mixer.music.set_volume(present_vol)
        volume_btn.configure(image=un_mute_icon)
        muted = False


# Mute/Un-mute Button
mute_icon = PhotoImage(file=r"Images/mute-button.png")  # Adding an icon for the mute button
un_mute_icon = PhotoImage(file=r"Images/un-mute-button.png")  # Adding an icon for the un-mute button
volume_btn = ttk.Button(bottom_frame, image=un_mute_icon, command=mute_music)  # Adding the mute/un-mute button
volume_btn.grid(row=0, column=0, pady=25, padx=15)


# Defining a scale to control the volume level
def set_vol(val):
    volume = float(val) / 100  # set_volume takes value only from 0-1
    mixer.music.set_volume(volume)


# Volume scale
vol_control = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)  # Creating a volume scale
vol_control.set(50)
mixer.music.set_volume(0.5)
vol_control.grid(row=0, column=1, pady=25, padx=15)


# Modifying the close button of the GUI
def close_button():
    mixer.music.stop()
    root_var.destroy()


root_var.protocol("WM_DELETE_WINDOW", close_button)

# Loop of the GUI
root_var.mainloop()