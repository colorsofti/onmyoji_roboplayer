# coding=utf-8

import pyautogui
import time

time.sleep(5)

screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(1914, 257)
pyautogui.dragTo(1911, 377, duration=0.5, button='left')


