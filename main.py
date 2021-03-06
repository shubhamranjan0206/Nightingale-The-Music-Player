!pip install mutagen 
!pip install ttkthemes

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer
import os
import time
import threading
from mutagen.mp3 import MP3
from tkinter import ttk
import ttkthemes

#ttk stands for themed widgets and is used for making labels and buttons look better

def music_length(song_to_be_played):
    #os.path.splitext() can be used to extract extensions from filename
    file_data=os.path.splitext(song_to_be_played) 
    if file_data[1]=='.mp3':
        audio=MP3(song_to_be_played)
        total_length=audio.info.length
    else:
        a=mixer.Sound(song_to_be_played)
        total_length=a.get_length() #total_length variable value is in seconds
    mins, secs=divmod(total_length, 60)
    mins=round(mins)
    secs=round(secs)
    time='{:02d}:{:02d}'.format(mins, secs) #this is called format string 
    lengthlabel['text'] = "Total Length" + ' - ' + time
    thread1=threading.Thread(target=current_length,args=(total_length,))
    thread1.start()
    #this thread will be destroyed once the function linked with the thread is executed(ie when stop func is pressed
    #or song is played upto end)

#Here Threading is necessary because when current_length funct will be called our program will run while loop for 
#time= total_length of music and during that particular time we won't be able to use other widgets/features. hence,
#multitasking is needed and thus, we use Threading .

def current_length(temp):
    while(temp and mixer.music.get_busy()):
        #mixer.music.get_busy() returns false when music is stopped
        global paused
        if paused:
            continue
        else:
            mins, secs=divmod(temp, 60)
            mins=round(mins)
            secs=round(secs)
            time_='{:02d}:{:02d}'.format(mins, secs) #this is called format string 
            currenttimelabel['text'] = "Current Length" + ' - ' + time_
            time.sleep(1)
            temp-=1


paused=False
def play_btn():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music is Resumed"
        paused = FALSE
    else:
        try:
            stop_btn()
            time.sleep(1)
            #the above two steps are important for currenttimelabel to behave accurately bcz when one music is playing
            #and we select and play some other music from the playlist without stopping the current song then when 
            #play_btn  func is called , instead of quitting the ongoing thread an additional thread will be created
            #and unexpected behaviour will be observed
            
            #curselection() func return a tuple containing pos of selected list item
            selected_song=lb.curselection()
            selected_song=int(selected_song[0])
            song_to_be_played=playlist[selected_song]
            mixer.music.load(song_to_be_played)
            mixer.music.play()
            #changing the status of statusbar
            statusbar['text']='music is playing'+'-'+os.path.basename(song_to_be_played)
            music_length(song_to_be_played)
            
        except:
            messagebox.showerror('File not found', 'File not found')

def stop_btn():
    mixer.music.stop()
    #changing the status of statusbar
    statusbar['text']='music is stopped'
    
def pause_btn():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text']="music is paused"
    
def set_vol(val):
    #in tkinter whenever a function is called using widget then the value is stored in a variable val
    #so when u slide the scale widget the value will be stored in val variable
    volume=float(val)/100
    #this step is imp bcz only accepts value between 0 and 1
    mixer.music.set_volume(volume)

def about_us():
    messagebox.showinfo('Nightingale','Developer - Shubham Ranjan')

#Playlist contains the list of path of songs that are added in the list box
playlist=[]

def open_file():
    global filename
    filename=filedialog.askopenfilename()
    add_song_to_playlist()

def add_song_to_playlist():
    index=0
    lb.insert(index,os.path.basename(filename))
    playlist.insert(index,filename)
    #index+=1

muted=False
def mute_btn():
    global muted
    if muted:
        volbtn.config(image=volphoto)
        mixer.music.set_volume(0.60)
        scale.set(60)
        muted=False
        statusbar['text']='volume is unmuted'
    else:
        volbtn.config(image=mutephoto)
        mixer.music.set_volume(0)
        scale.set(0)
        muted=True 
        statusbar['text']='volume is muted'

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop_btn()
        root.destroy()

def del_song():
    selected_song=lb.curselection()
    selected_song=int(selected_song[0])
    lb.delete(selected_song)
    playlist.pop(selected_song)

def exit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = ttkthemes.themed_tk.ThemedTk()
root.get_themes()               
root.set_theme("radiance")

#setting size of root window
#root.geometry('500x500')
#setting title of the root window
root.title("Nightingale-The Music Player")

text = ttk.Label(root, text='welcome to the best music player of the century',relief=SUNKEN)
text.pack(fill=X,pady=10,padx=10)

frame=Frame(root)
frame.pack()

leftframe=Frame(frame)
leftframe.pack(side=LEFT)

rightframe=Frame(frame)
rightframe.pack(side=LEFT)

topframe=Frame(rightframe)
topframe.pack()

lb=Listbox(leftframe)
lb.pack(padx=10,pady=10)

addbtn=ttk.Button(leftframe,text='+add',command=open_file)
addbtn.pack(side=LEFT,padx=20)

delbtn=ttk.Button(leftframe,text='-del',command=del_song)
delbtn.pack()

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open",command=open_file)
subMenu.add_command(label="Exit",command=exit)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us",command= about_us)

#initializing the mixer
mixer.init()

#creating label to display total length of the music
lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack()

#creating label to display current remaing time
currenttimelabel = ttk.Label(topframe, text='current time : --:--')
currenttimelabel.pack(pady=10)

buttonframe=Frame(rightframe,relief=RAISED,borderwidth=1)
buttonframe.pack(padx=10)

#play button
#creating image variable to include image in button
style = ttk.Style()
style.configure('W.TButton', font =
               ('calibri', 10, 'bold'),
                background = 'red',foreground = 'red')

playbtn=ttk.Button(buttonframe,text ="Play",command=play_btn,style = 'W.TButton')
playbtn.grid(row=0,column=0)

#stop button
# photo2=PhotoImage(file='./stop.png')
stopbtn=ttk.Button(buttonframe,text ="Stop",command=stop_btn,style = 'W.TButton')
stopbtn.grid(row=0,column=1)

#pause button
# photo3=PhotoImage(file='./pause.png')
pausebtn=ttk.Button(buttonframe,text ="Pause",command=pause_btn,style = 'W.TButton')
pausebtn.grid(row=0,column=2)

bottomframe=Frame(rightframe)
bottomframe.pack(padx=10)

#rewind button
# photo4=PhotoImage(file='./rewind.png')
rewindbtn=ttk.Button(bottomframe,text ="Rewind",command=play_btn,style = 'W.TButton')
rewindbtn.grid(row=0,column=0)

# mutephoto=PhotoImage(file='./mute.png')
# volphoto=PhotoImage(file='./vol.png')
volbtn=ttk.Button(bottomframe,text ="volume/mute",command=mute_btn,style = 'W.TButton')
volbtn.grid(row=0,column=1)

scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
#this will show default value of scale to 100
scale.set(60)
#this will set default value to 100
mixer.music.set_volume(100)
scale.grid(row=0,column=2)

statusbar=ttk.Label(root,text='nightingale version 1.0 is running!!',relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X,pady=10,padx=10) #bottom is used so as to to make statusbar appear at bottom of root window
#fill paramter is used for spanning of statusbar .x means spanning along x axis

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

