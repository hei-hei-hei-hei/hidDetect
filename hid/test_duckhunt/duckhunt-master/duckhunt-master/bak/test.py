import pyautogui
import time

time.sleep(3)

text = "hello world"


for char in text:
    pyautogui.typewrite(char)
    time.sleep(0.1)

pyautogui.press('enter')