import win32gui, win32com.client
import keyboard as kb
import time
import psutil

hwnd: int
x:int
y:int
w:int
h:int
midY = 513
midX = 1775
windowSet = False
running = True

def keepUpTime():
    if windowSet:
        return 10
    else:
        return 1

def winEnumHandler(temphwnd, ctx):
    global running
    global windowSet
    global hwnd
    if win32gui.IsWindowVisible(temphwnd):
        # print ( hex(temphwnd), win32gui.GetWindowText(temphwnd) )
        if win32gui.GetWindowText(temphwnd) == "Spotify - Web Player: Music for everyone" or win32gui.GetWindowText(temphwnd) == "Songs I would listen to if I listened to music - playlist by a.Toby.a | Spotify":
            hwnd = temphwnd
            print("window found!")
            newPosition()
            windowSet = True

def checkSpotify():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == "Spotify.exe":
            print("spotify found")
            return True
    return False

def checkWindow():
    global windowSet
    global hwnd
    windowSet = True
    foregroundWindow = win32gui.GetForegroundWindow()
    windowText = win32gui.GetWindowText(foregroundWindow)
    hwnd = win32gui.FindWindow(None, windowText)
    newPosition()

def focusWindow():
    global windowSet
    if windowSet:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    
def checkY(dir):
    if y < midY:
        return 0
    else:
        if dir == "l":
            if x <= 1913:
                return 1027
            else:
                return 989
        elif dir == "r":
            if x >= 1624:
                return 989
            else:
                return 1027

def moveWindowUp():
    global windowSet
    try:
        newPosition()
        if windowSet:
            if x > midX:
                if x <= 2663:
                    moveWindow(1913, 0)
                else:
                    moveWindow(3544, 0)
            elif x <= midX:
                if x <= 887:
                    moveWindow(-7, 0)
                else:
                    moveWindow(1624, 0)
    except:
        windowSet = False
        print("window not found")
def moveWindowDown():
    global windowSet
    try:
        newPosition()
        if windowSet:
            if x > midX:
                if x <= 2663:
                    moveWindow(1913, 989)
                else:
                    moveWindow(3544, 989)
            elif x <= midX:
                if x <= 887:
                    moveWindow(-7, 1027)
                else:
                    moveWindow(1624, 1027)
    except:
        windowSet = False
        print("window not found")
def moveWindowLeft():
    global windowSet
    try:
        newPosition()
        if windowSet:
            if x > 1913:
                moveWindow(1913, checkY("l"))
            elif x <= 1913 and x > 1624:
                moveWindow(1624, checkY("l"))
            else:
                moveWindow(-7, checkY("l"))
    except:
        windowSet = False
        print("window not found")
def moveWindowRight():
    global windowSet
    try:
        newPosition()
        if windowSet:
            if x < 1624:
                moveWindow(1624, checkY("r"))
            elif x >= 1624 and x < 1913:
                moveWindow(1913, checkY("r"))
            else:
                moveWindow(3544, checkY("r"))
    except:
        windowSet = False
        print("window not found")
        
def moveWindow(x, y):
        win32gui.MoveWindow(hwnd, x, y, 303, 50, True)
    
def newPosition():
    global x
    global y
    global w
    global h
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))


# kb.add_hotkey('ctrl+shift+m', checkWindow)
kb.add_hotkey('ctrl+shift+3', focusWindow)
kb.add_hotkey('ctrl+shift+up', moveWindowUp)
kb.add_hotkey('ctrl+shift+down', moveWindowDown)
kb.add_hotkey('ctrl+shift+left', moveWindowLeft)
kb.add_hotkey('ctrl+shift+right', moveWindowRight)

while running:
    print("checking open windows")
    windowSet = False
    foundSpotify = False
    win32gui.EnumWindows(winEnumHandler, None)
    print("checking spotify")
    foundSpotify = checkSpotify()
    if foundSpotify == False:
        print ("spotify not found")
        running = False
    time.sleep(keepUpTime())



