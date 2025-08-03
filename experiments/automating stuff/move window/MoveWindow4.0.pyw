import subprocess
import win32gui, win32com.client
from threading import Thread
import keyboard as kb
import signal
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

# farL = -7
# midL = 953
# midX = 1913
# midR = 2873
# baseFarR = 3847
# farR: int
# top:int = 0
# baseBotL = 1087
# botL: int
# midLY = 540
# baseBotR = 1049
# botR: int
# midRY = 521

farL = -1927
midL = -967
midX = -7
midR = 953
baseFarR = 1927
farR: int
top:int = 0
baseBotL = 1049
botL: int
midLY = 521
baseBotR = 1087
botR: int
midRY = 540

#-------------------------------------------------------------------------

def startSpotify():
    print('starting spotify')
    while subprocess.run('C:\\Users\\Toby\\AppData\\Roaming\\Spotify\\Spotify.exe'):
        os.kill(os.getpid(), signal.SIGINT)

def getMiniplayerId(temphwnd, ctx):
    global windowSet, miniplayerId, firstFind
    if not windowSet:
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
        global spotifyId
        if win32gui.IsWindowVisible(temphwnd):
            if win32gui.GetWindowText(temphwnd) == "Spotify":
                print('found spotify')
                spotifyId = temphwnd
                spotifySet = True
                return
                
def spotifyFocus():
    if win32gui.GetForegroundWindow() == spotifyId:
        print(f"spotify in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return True
    else:
        print(f"spotify not in focus, {spotifyId}, {win32gui.GetForegroundWindow()}.")
        return False

#-------------------------------------------------------------------------

def focusWindow():
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(miniplayerId)
    time.sleep(0.2)
            
def getPosSize():
    global x, y, w, h, farR, botL, botR, baseFarR, baseBotL, baseBotR
    rect = win32gui.GetWindowRect(miniplayerId)
    x = rect[0]
    y = rect[1]
    w = rect[2]-x
    h = rect[3]-y
    farR = baseFarR - w
    botL = baseBotL - h
    botR = baseBotR - h
    # print("Window %s:" % win32gui.GetWindowText(miniplayerId))
    print("\tLocation: (%d, %d)" % (x, y))
    # print("\t    Size: (%d, %d)" % (w, h))     
    print(f"miniplayer ID - {miniplayerId}")
    realX = x + (w / 2)
    realY = y + (h / 2)
    if realX < midL:
        if realY < midLY:
            return(1)
        else:
            return(2)
    elif realX < midX:
        if realY < midLY:
            return(3)
        else:
            return(4)
    elif realX < midR:
        if realY < midRY:
            return(5)
        else:
            return(6)
    else:
        if realY < midRY:
            return(7)
        else:
            return(8)
        
    
def resetWindow():
    global w, h
    w = 303
    h = 60
    moveWindow()
    setPos("R")
    
def setPos(dir):
    global x, y, w, h
    pos = getPosSize()
    print(pos)
    if dir == 'U' or dir == 'D':
        y = setPosY(dir, pos, True)
    elif dir == 'L' or dir == 'R':
        x = setPosX(dir, pos, True)
    else:
        print('something went wrong')
    moveWindow()

def setPosY(dir, pos, origin):
    global x, w, h
    if dir == 'D':
        if pos < 5:
            y = botL
        else:
            y =  botR
    else:
        y = top
    if origin:
        if pos < 3 or (pos > 4 and pos < 7):
            x = setPosX('L', pos + 2, False)
        else:
            x = setPosX('R', pos - 2, False)
    return y

def setPosX(dir, pos, origin):
    global y, w, h
    if dir == 'L':
        if pos < 5:
            x = farL
        elif pos < 7:
            x = midX - w + 14
        else:
            x = midX
    else:
        if pos < 3:
            x = midX - w + 14
        elif pos < 5:
            x = midX
        else:
            x = farR
    if origin:
        if (pos/2).is_integer():
                if (pos == 5 or pos == 6) and dir == 'L':
                    y = setPosY('D', 4, False)
                elif (pos == 3 or pos == 4) and dir == 'R':
                    y = setPosY('D', 5, False)
                else:
                    y = setPosY('D', pos, False)
        else:
                y = setPosY('U', pos, False)
    return x
    
def moveWindow():
    global x, y, w, h
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Spotify - Web Player: Music for everyone":
        focusWindow()
    win32gui.MoveWindow(miniplayerId, x, y, w, h, True)
    
#-------------------------------------------------------------------------

def upCheck():
    while True:
        kb.wait('ctrl+shift+up')
        if windowSet:
            doEvent(upEvent)
        
def downCheck():
    while True:
        kb.wait('ctrl+shift+down')
        if windowSet:
            doEvent(downEvent)
        
def leftCheck():
    while True:
        kb.wait('ctrl+shift+left')
        if windowSet:
            doEvent(leftEvent)
        
def rightCheck():
    while True:
        kb.wait('ctrl+shift+right')
        if windowSet:
            doEvent(rightEvent)
        
def resetCheck():
    while True:
        kb.wait('ctrl+shift+r')
        if windowSet:
            doEvent(resetEvent)
        
def clickCheck():
    while True:
        mouse.wait('left', 'up')
        clickEvent()
                
def doEvent(func):
    global windowSet, firstFind
    try:
        func()
    except:
        print('something went wrong, likely mini player doesn\'t exist')
        windowSet = False
        firstFind = True
        win32gui.EnumWindows(getMiniplayerId, None)
        

#-------------------------------------------------------------------------
        
def upEvent():
    setPos("U")
        
def downEvent():
    setPos("D")
        
def leftEvent():
    setPos("L")
        
def rightEvent():
    setPos("R")
        
def clickEvent():
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