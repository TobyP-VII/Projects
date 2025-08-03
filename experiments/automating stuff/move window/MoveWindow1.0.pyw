import win32gui, win32com.client
import keyboard as kb
import time
import psutil

hwnd: int
windowSet = False
running = True
firstFind = True
x: int
y: int
w: int
h: int

#####

def winEnumHandler(temphwnd, ctx):
    global windowSet, hwnd, firstFind
    if win32gui.IsWindowVisible(temphwnd):
        # print ( hex(temphwnd), win32gui.GetWindowText(temphwnd) )
        if win32gui.GetWindowText(temphwnd) == "Spotify - Web Player: Music for everyone":
            hwnd = temphwnd
            getPosSize()
            windowSet = True
            if firstFind:
                firstFind = False
                setX("R")
            
def checkSpotify():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == "Spotify.exe":
            print("spotify found")
            return True
    return False

#####

def focusWindow():
    print ("focussing window")
    global windowSet
    if windowSet:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.2)
            
def getPosSize():
    global x, y, w, h
    if windowSet:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2]-x
        h = rect[3]-y
        print("Window %s:" % win32gui.GetWindowText(hwnd))
        print("\tLocation: (%d, %d)" % (x, y))
        print("\t    Size: (%d, %d)" % (w, h))     
    
def miniWindow():
    print ("resizing window")
    global x, y, w, h
    getPosSize()
    w = 303
    h = 60
    moveWindow()
    
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
    
def moveWindow():
    global x, y, w, h
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Spotify - Web Player: Music for everyone":
        focusWindow()
    print("moving window")
    win32gui.MoveWindow(hwnd, x, y, w, h, True)
    
#####
    
# kb.add_hotkey('ctrl+shift+3', focusWindow)
kb.add_hotkey('ctrl+shift+up', lambda: setY("U"))
kb.add_hotkey('ctrl+shift+down', lambda: setY("D"))
kb.add_hotkey('ctrl+shift+left', lambda: setX("L"))
kb.add_hotkey('ctrl+shift+right', lambda: setX("R"))
kb.add_hotkey('ctrl+shift+r', miniWindow)

while running:
    if windowSet:
        time.sleep(10)
    else:
        time.sleep(1.5)
    if not checkSpotify():
        running = False
    windowSet = False
    win32gui.EnumWindows(winEnumHandler, None)
    