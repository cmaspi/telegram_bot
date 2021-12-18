import pyautogui as spammer
import time

time.sleep(3)
string='optin'
t=time.time()

while time.time()-t < 15:
    spammer.write(string)
    spammer.press('enter')