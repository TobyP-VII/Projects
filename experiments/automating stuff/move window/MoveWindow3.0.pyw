import subprocess
import win32gui, win32com.client
from threading import Thread
import keyboard as kb
import signal
import psutil
import mouse
import time
import os

#-------------------------------------------------------------------------

windowSet = False
spotifySet = False
firstFind = True
spotifyId: int
miniplayerId: int
x: int
y: int
w: int
h: int

#-------------------------------------------------------------------------

def startSpotify():
    print('starting spotify')
    while subprocess.run('C:\\Users\\Toby\\AppData\\Roaming\\Spotify\\Spotify.exe'):
        os.kill(os.getpid(), signal.SIGINT)

def getMiniplayerId(temphwnd, ctx):
    global windowSet, miniplayerId, firstFind
    if not windowSet:
        print('getting miniplayer ID')
        if win32gui.IsWindowVisible(temphwnd):
            if win32gui.GetWindowText(temphwnd) == "Spotify - Web Player: Music for everyone":
                print('found miniplayer')
                miniplayerId = temphwnd
                windowSet = True
                if firstFind:
                    firstFind = False
                    getPosSize()
                    resetWindow()
                return
                
def getSpotifyId(temphwnd, ctx):
    global spotifySet
    if not spotifySet:
        print('getting spotify ID')
        global spotifyId
        if win32gui.IsWindowVisible(temphwnd):
            if win32gui.GetWindowText(temphwnd) == "Spotify":
                print('found sportify')
                spotifyId = temphwnd
                spotifySet = True
                return
                
def spotifyFocus():
    print('checking if spotify is in focus')
    if win32gui.GetForegroundWindow() == spotifyId:
        print(f"spotify in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return True
    else:
        print(f"spotify not in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return False

#-------------------------------------------------------------------------

def focusWindow():
    print ("focussing window")
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(miniplayerId)
    time.sleep(0.2)
            
def getPosSize():
    print("getting pos and size")
    global x, y, w, h
    rect = win32gui.GetWindowRect(miniplayerId)
    x = rect[0]
    y = rect[1]
    w = rect[2]-x
    h = rect[3]-y
    # print("Window %s:" % win32gui.GetWindowText(miniplayerId))
    # print("\tLocation: (%d, %d)" % (x, y))
    # print("\t    Size: (%d, %d)" % (w, h))     
    print(f"miniplayer ID - {miniplayerId}")
    
def resetWindow():
    print('resetting window')
    global w, h
    w = 303
    h = 60
    moveWindow()
    setX("R")
    setY("D")
    
def setX(dir):
    global x, y, w, h
    getPosSize()
    print(f"{dir} dir pressed")
    if dir == "L":
        if x <= (1913 - w+14):
            x = -7
        elif x <= 1913:
            x = (1913 - w+14)
        elif x <= (3833 - w+14):
            x = 1913
        else:
            x = (3833 - w+14)
        if x <= (1913 - ((w+14)/2)):
            if y >= 1087/2:
                y = (1087 - h)
            else:
                y = 0
        else:
            if y >= 1087/2:
                y = (1049 - h)
            else:
                y = 0
    else:
        if x >= 1913:
            x = (3833 - w+14)
        elif x >= (1913 - w+14):
            x = 1913
        elif x >= -7:
            x = (1913 - w+14)
        else:
            x = -7
        if x >= (1913 - ((w+14)/2)):
            if y >= 1087/2:
                y = (1049 - h)
            else:
                y = 0
        else:
            if y >= 1087/2:
                y = (1087 - h)
            else:
                y = 0
    moveWindow()
        
def setY(dir):
    global x, y, w, h
    getPosSize()
    print(f"{dir} dir pressed")
    if dir == "U":
        y = 0
    else:
        if x <= (1913 - (w-14)/2):
            y = (1087 - h)
        else:
            y = (1049 - h)
    if x <= (1913 - w+14)/2:
        x = -7
    elif x <= (1913 - (w+14)/2):
        x = (1913 - w+14)
    elif x <= (3833 - w+14)-((1913 - (w-14))/2):
        x = 1913
    else:
        x = (3833 - w+14)
    moveWindow()
    
def moveWindow():
    print("moving window")
    global x, y, w, h
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Spotify - Web Player: Music for everyone":
        focusWindow()
    win32gui.MoveWindow(miniplayerId, x, y, w, h, True)
    
#-------------------------------------------------------------------------

def upCheck():
    while True:
        kb.wait('ctrl+shift+up')
        if windowSet:
            upEvent()
        
def downCheck():
    while True:
        kb.wait('ctrl+shift+down')
        if windowSet:
            downEvent()
        
def leftCheck():
    while True:
        kb.wait('ctrl+shift+left')
        if windowSet:
            leftEvent()
        
def rightCheck():
    while True:
        kb.wait('ctrl+shift+right')
        if windowSet:
            rightEvent()
        
def clickCheck():
    while True:
        mouse.wait('left', 'up')
        clickEvent()
        
def resetCheck():
    while True:
        kb.wait('ctrl+shift+r')
        if windowSet:
            resetEvent()

#-------------------------------------------------------------------------
        
def upEvent():
    print('pressed up')
    setY("U")
        
def downEvent():
    print('pressed down')
    setY("D")
        
def leftEvent():
    print('pressed left')
    setX("L")
        
def rightEvent():
    print('pressed right')
    setX("R")
        
def clickEvent():
    print('clicked')
    global windowSet
    try:
        if not spotifySet:
            print('spotify not set')
            win32gui.EnumWindows(getSpotifyId, None)
        if spotifySet and not windowSet:
            if spotifyFocus():
                time.sleep(0.3)
                print('window not set')
                win32gui.EnumWindows(getMiniplayerId, None)
    except:
        print('something went wrong')

def resetEvent():
    print('pressed reset')
    resetWindow()
        
        

#-------------------------------------------------------------------------

print("starting t1")
t1 = Thread(target = startSpotify)
print("starting t2")
t2 = Thread(target = upCheck)
print("starting t3")
t3 = Thread(target = downCheck)
print("starting t4")
t4 = Thread(target = leftCheck)
print("starting t5")
t5 = Thread(target = rightCheck)
print("starting t6")
t6 = Thread(target = clickCheck)
print("starting t7")
t7 = Thread(target = resetCheck)


t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()