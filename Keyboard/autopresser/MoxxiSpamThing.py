from pynput.keyboard import Controller, Listener
import time



try:
    keyboard = Controller()
    presskey = "q"
    times = int(input("\nHow many THOUSANDS do you want to hand over to moxxi per press?\n"))
    times -= 1
    delaytime = float(0)
    input("\npress enter to continue")
        
    print("Ready")

    def on_press(key):
        key = str(key)
        key = key.replace("'", "")
        print(key)
        if str(key) == ("\\x11"):
            for number in range(times):
                keyboard.press(presskey)
                keyboard.release(presskey)
                time.sleep(delaytime)
            time.sleep(5)

    with Listener(on_press=on_press) as listener:
        listener.join()
            
except(Exception): 
	print("An error occured")