

    

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

if __name__ == '__main__':
    while True:
        if (keyboard.is_pressed(start_key)):
            pyautogui.click()

            pyautogui.click()

            pyautogui.click()

            pyautogui.click()

            pyautogui.click()

            pyautogui.click()
