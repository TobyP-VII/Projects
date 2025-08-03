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
firstFind = True
spotifyId: int
miniplayerId: int
x: int
y: int
w: int
h: int

#-------------------------------------------------------------------------

def winEnumHandler(temphwnd, ctx):
    global windowSet, miniplayerId, firstFind
    if win32gui.IsWindowVisible(temphwnd):
        if win32gui.GetWindowText(temphwnd) == "Spotify - Web Player: Music for everyone":
            miniplayerId = temphwnd
            windowSet = True
            if firstFind:
                firstFind = False
                getPosSize()
                resetWindow()
                
def getSpotifyId(temphwnd, ctx):
    global spotifyId
    if win32gui.IsWindowVisible(temphwnd):
        if win32gui.GetWindowText(temphwnd) == "Spotify":
            spotifyId = temphwnd
                
def spotifyFocus():
    if win32gui.GetForegroundWindow() == spotifyId:
        print(f"spotify in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return True
    else:
        print(f"spotify not in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return False
                       
def checkSpotify():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == "Spotify.exe":
            print("spotify found")
            return True
    return False

#-------------------------------------------------------------------------

def focusWindow():
    print ("focussing window")
    global windowSet
    if windowSet:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(miniplayerId)
    time.sleep(0.2)
            
def getPosSize():
    global x, y, w, h
    print("getting pos and size")
    if windowSet:
        rect = win32gui.GetWindowRect(miniplayerId)
        x = rect[0]
        y = rect[1]
        w = rect[2]-x
        h = rect[3]-y
        # print("Window %s:" % win32gui.GetWindowText(miniplayerId))
        # print("\tLocation: (%d, %d)" % (x, y))
        # print("\t    Size: (%d, %d)" % (w, h))     
        print(f"miniplayer ID - {miniplayerId}")
    else:
        print("miniplayer not found")
    
def resetWindow():
    global w, h
    if windowSet:
        w = 303
        h = 60
        moveWindow()
        setX("R")
        setY("D")
    
def setX(dir):
    global x, y, w, h
    if windowSet:
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
    else:
        print("miniplayer not found")
        
def setY(dir):
    global x, y, w, h
    if windowSet:
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
    else:
        print("miniplayer not found")
    
def moveWindow():
    global x, y, w, h
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Spotify - Web Player: Music for everyone":
        focusWindow()
    print("moving window")
    win32gui.MoveWindow(miniplayerId, x, y, w, h, True)
    
#-------------------------------------------------------------------------

def upCheck():
    while True:
        kb.wait('ctrl+shift+up')
        upEvent()
        
def downCheck():
    while True:
        kb.wait('ctrl+shift+down')
        downEvent()
        
def leftCheck():
    while True:
        kb.wait('ctrl+shift+left')
        leftEvent()
        
def rightCheck():
    while True:
        kb.wait('ctrl+shift+right')
        rightEvent()
        
def clickCheck():
    while True:
        mouse.wait('left', 'up')
        clickEvent()
        
def resetCheck():
    while True:
        kb.wait('ctrl+shift+r')
        resetEvent()

#-------------------------------------------------------------------------
        
def upEvent():
    setY("U")
        
def downEvent():
    setY("D")
        
def leftEvent():
    setX("L")
        
def rightEvent():
    setX("R")
        
def clickEvent():
    global windowSet
    spotifyInFocus = spotifyFocus()
    time.sleep(0.2)
    if spotifyInFocus:
        windowSet = False
        win32gui.EnumWindows(winEnumHandler, None)
    else:
        if not checkSpotify():
            os.kill(os.getpid(), signal.SIGINT)
    pass

def resetEvent():
    global windowSet, w, h
    if windowSet:
        resetWindow()
        
        

#-------------------------------------------------------------------------

for i in range (10):
    time.sleep(1)
    if checkSpotify():
        win32gui.EnumWindows(getSpotifyId, None)
        break
    if i == 9:
        os.kill(os.getpid(), signal.SIGINT)

t1 = Thread(target = upCheck)
t2 = Thread(target = downCheck)
t3 = Thread(target = leftCheck)
t4 = Thread(target = rightCheck)
t5 = Thread(target = clickCheck)
t6 = Thread(target = resetCheck)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()