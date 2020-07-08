import os, time, threading, getpass
from mutagen.mp3 import MP3
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from ttkthemes import themed_tk as themetk
from pygame import mixer
from tinytag import TinyTag

# GUI creation
root_var = themetk.ThemedTk()  # Setting the the theme

# root_var.get_themes()
# root_var.set_theme("")

root_var.title("MP3 Player")  # Program name (title on GUI)
root_var.iconbitmap(r"Icons/music_note.ico")  # Setting an icon & it's location

"""
Major components of the 'root_var' are STATUS_BAR, LEFT_FRAME, RIGHT_FRAME
    *RIGHT FRAME -> PlayList
    *LEFT FRAME -> TOP_FRAME, MIDDLE_FRAME, BOTTOM_FRAME  
"""

# Status Bar
username = getpass.getuser()  # We use the getpass module to get the name of the current user
# status_bar = Label(root_var, text="Welcome " + username, anchor=SW)
status_bar = Label(root_var, text="Welcome Christopher", anchor=SW)
status_bar.pack(side=BOTTOM, fill=X)

mixer.init()  # Initializing the mixer module

# Menu Bar
menu_bar = Menu(root_var)  # Initializing an empty menu bar
root_var.config(menu=menu_bar)


# Defining a function to browse and select a file from the user's desktop
def select_file():
    global filename
    filename = filedialog.askopenfilename()
    if filename is not "":
        exact_filename = os.path.basename(filename)  # Exact filename without the path
        add_to_playlist(exact_filename)
    else:
        print("Did not select a file when user went to browse!")


# Defining a function to add files to the playlist box
def add_to_playlist(received_file_name):
    index = 0
    playlist_box.insert(index, received_file_name)  # Adding the file to the playlist in the GUI
    playlist_array.insert(index, filename)  # Adding the file path to the playlist array
    playlist_box.pack()
    index += 1


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
        file.seek(22)
        file.truncate()
        file.seek(21)
        file.write("\n")
        file.seek(0)


# Sub Menu Bar
sub_menu = Menu(menu_bar, tearoff=0)  # Initializing a sub menu (no#1)
menu_bar.add_cascade(label="File", menu=sub_menu)  # Creating a bar with the name 'File', and it has a sub menu
sub_menu.add_command(label="Open", command=select_file)  # Creating a sub menu with the name 'Open'
sub_menu.add_command(label="Clear History", command=clear_history)  # Creating a sub menu to clear song history log
sub_menu.add_command(label="Exit", command=root_var.destroy)  # Creating a sub menu with the name 'Exit'


# Defining a fn to display the following message on clicking About from Help
def about_us():
    messagebox.showinfo("About *ENTER SOFTWARE NAME*", '''*ENTER SOFTWARE NAME* is a simple audio player, that was developed as a learning project.
    Created By:- 
        Christopher J.S.
    If you wish to make a contribution to this software, email me at christo77793@gmail.com''')


# Sub Menu Bar
sub_menu = Menu(menu_bar, tearoff=0)  # Initializing a sub menu (no#2)
menu_bar.add_cascade(label="Help", menu=sub_menu)  # Creating a bar with the name 'Help', and it has a sub menu
sub_menu.add_command(label="About", command=about_us)  # Creating a sub menu with the name 'About'

# Creating frames to improve design of our GUI

right_frame = Frame(root_var)  # Right Frame
right_frame.pack(side=RIGHT, padx=15)

left_frame = Frame(root_var)  # Left Frame
left_frame.pack(side=LEFT, padx=15)

top_frame = Frame(left_frame)  # Top Frame
top_frame.pack()

# Creating a playlist

playlist_array = []

playlist_box_scrollbar = Scrollbar(right_frame, orient=VERTICAL)  # Creating a scrollbar for the playlist

playlist_box = Listbox(right_frame, width=25, background="lightgray", bd=0, yscrollcommand=playlist_box_scrollbar.set)
playlist_box_scrollbar.config(command=playlist_box.yview)
playlist_box_scrollbar.pack(side=RIGHT, fill=Y)
playlist_box.pack()

add_song_icon = PhotoImage(file=r"Images/add_song.png")  # Adding an icon for the add songs button
add_song_btn = Button(right_frame, image=add_song_icon, bd=0, command=select_file)  # A button to add songs to the list
add_song_btn.pack(side=LEFT, pady=9, padx=15)

del_song_icon = PhotoImage(file=r"Images/del_song.png")  # Adding an icon for the delete songs button
del_song_btn = Button(right_frame, image=del_song_icon, bd=0, command=del_file)  # A button to delete songs from the list
del_song_btn.pack(side=RIGHT, pady=9, padx=15)


# Defining a set of functions to repeat songs
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
            test = get_time()
            unloop_song(test)
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
rep_song_btn = Button(right_frame, image=rep_song_off_icon, bd=0, command=rep_song)  # A button to delete songs from the list
rep_song_btn.pack(pady=9)

# Audio file details

audio_length = Label(top_frame, text="Add a song to start listening to some music")  # Displays audio length in the play fn
audio_length.pack(pady=15, padx=5)

remaining_audio_time = Label(top_frame, text="")  # Displays the current time of the audio
remaining_audio_time.pack()


# Defining a function to display audio details
def audio_details(to_play):
    file_extension = os.path.splitext(to_play)

    if file_extension[1] == ".mp3":
        sound_file = MP3(to_play)
        file_time_span = sound_file.info.length
    else:
        sound_file = mixer.Sound(to_play)
        file_time_span = sound_file.get_length()

    mins, secs = divmod(file_time_span, 60)
    mins = round(mins)
    secs = round(secs)
    total_time_format = "{:02d}:{:02d}".format(mins, secs)
    audio_length["text"] = "Audio Length:- " + total_time_format

    # Applying the concept of threads to isolate the execution of the while loop in the start_count fn
    t1 = threading.Thread(target=start_count, args=(file_time_span,))
    t1.start()


# Defining a function to display the current time of the audio
def start_count(test):
    global to_un_pause, restart_time
    current_time = 0
    while current_time <= test and mixer.music.get_busy():
        if to_un_pause:
            continue
        else:
            if restart_time:
                current_time = 0
                restart_time = False
            else:
                pass
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            current_time_format = "{:02d}:{:02d}".format(mins, secs)
            remaining_audio_time["text"] = "Currently at- " + current_time_format
            time.sleep(1)
            current_time += 1
    remaining_audio_time["text"] = ""
    audio_length["text"] = "Last played song:- " + os.path.basename(to_play)


# Defining a button to play music
def play_button(repeat):
    global to_un_pause, paused, check_val, allow_repeat, to_play
    if to_un_pause:
        mixer.music.unpause()  # Resumes the music from when it was paused
        to_un_pause = False
        selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
        selected_song = int(selected_song[0])  # Converts tuple to int
        to_play = playlist_array[selected_song]  # Provides the file path from the playlist array
        song_metadata = TinyTag.get(to_play)
        bitrate = song_metadata.bitrate
        song_offset = song_metadata.audio_offset
        status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset)
    else:
        try:
            mixer.music.stop()
            time.sleep(1)
            selected_song = playlist_box.curselection()  # Returns a tuple of with index no.
            selected_song = int(selected_song[0])  # Converts tuple to int
            to_play = playlist_array[selected_song]  # Provides the file path from the playlist array
            mixer.music.load(to_play)
            mixer.music.play(repeat)
            song_metadata = TinyTag.get(to_play)
            bitrate = song_metadata.bitrate
            song_offset = song_metadata.audio_offset
            audio_details(to_play)
            check_val = True
            paused = True
            allow_repeat = True
            song_heard = song_counter()
            if song_heard > 1:
                status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset) + " | You have heard this song " + str(song_heard) + " times"
            else:
                status_bar["text"] = "Bitrate: " + str(bitrate) + " | Audio Offset: " + str(song_offset)

        except Exception:
            # Since no file has been selected the following code will be executed
            messagebox.showwarning("Warning", "No file has been selected to play!")


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


# Defining a button to stop music
check_val = False


def stop_button():
    global check_val
    if check_val:
        mixer.music.stop()
        status_bar["text"] = "Music stopped!"  # Setting the status as stopped
        audio_length["text"] = "Last played song:- " + os.path.basename(to_play)
        remaining_audio_time["text"] = ""
    else:
        # Setting the status to show nothing is being played if user hits stop when no music is being played
        status_bar["text"] = "No music is being played to stop!"


# Defining a scale to control the volume level
def set_vol(val):
    volume = float(val) / 100  # set_volume takes value only from 0-1
    mixer.music.set_volume(volume)


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


# Creating a middle frame
middle_frame = Frame(left_frame)
middle_frame.pack(padx=35, pady=35)

# Play button
play_icon = PhotoImage(file=r"Images/play-button.png")  # Adding an icon for the play button
play_btn = Button(middle_frame, image=play_icon, bd=0, command=lambda: play_button(0))  # Adding the play button
play_btn.grid(row=0, column=0, padx=15)

# Pause button
pause_icon = PhotoImage(file=r"Images/pause-button.png")  # Adding an icon for the pause button
pause_btn = Button(middle_frame, image=pause_icon, bd=0, command=pause_button)  # Adding the play button
pause_btn.grid(row=0, column=1, padx=15)

# Stop button
stop_icon = PhotoImage(file=r"Images/stop-button.png")  # Adding an icon for the stop button
stop_btn = Button(middle_frame, image=stop_icon, bd=0, command=stop_button)  # Adding the stop button
stop_btn.grid(row=0, column=2, padx=15)

# Creating a bottom frame
bottom_frame = Frame(left_frame)
bottom_frame.pack()


# Defining a button to restart music
restart_time = False


def rewind_button():
    global restart_time
    restart_time = True
    mixer.music.rewind()


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


# Rewind button
rewind_icon = PhotoImage(file=r"Images/restart-button.png")  # Adding an icon for the rewind button
rewind_btn = Button(bottom_frame, image=rewind_icon, bd=0, command=rewind_button)  # Adding the stop button
rewind_btn.grid(row=0, column=0, padx=15)

# Mute/Un-mute Button
mute_icon = PhotoImage(file=r"Images/mute-button.png")  # Adding an icon for the mute button
un_mute_icon = PhotoImage(file=r"Images/un-mute-button.png")  # Adding an icon for the un-mute button
volume_btn = Button(bottom_frame, image=un_mute_icon, bd=0, command=mute_music)  # Adding the mute/un-mute button
volume_btn.grid(row=0, column=1, padx=5)

# Volume scale
vol_control = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)  # Creating a volume scale
vol_control.set(50)
mixer.music.set_volume(0.5)
vol_control.grid(row=0, column=2, pady=15, padx=30)


# Modifying the close button of the GUI
def close_button():
    mixer.music.stop()
    root_var.destroy()


root_var.protocol("WM_DELETE_WINDOW", close_button)

# Loop of the GUI
root_var.mainloop()