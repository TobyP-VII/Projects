

    

# while True:

#     click = input("Do you want to click?: ")
#     if click == "yes":
#         pyautogui.click()
#     else:
#         quit()

from pynput import keyboard
from pynput import mouse
from PIL import Image, ImageGrab
import pyautogui
import keyboard

start_key = 'p'
centre_colour = ''

def getHex(rgb):
    return '%02X%02X%02X'%rgb


def checkColour(x,y):
    bbox = (x,y,x+1,y+1)
    im = ImageGrab.grab(bbox=bbox)
    rgbim = im.convert('RGB')
    r,g,b = rgbim.getpixel((0,0))
    centre_colour = (r, g, b)
    print(f'COLOUR: {centre_colour}')

if __name__ == '__main__':
    while True:
        try:
            if (keyboard.is_pressed(start_key)):
                checkColour(960, 540)
        except:
            pass
