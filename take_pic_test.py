# coding=utf-8
from PIL import ImageGrab
import time
time.sleep(2)
im = ImageGrab.grab()
im.save("C:\\Users\\tannins\\Desktop\\PCVP\\yinyangshi\\pictures\\picGrapTest\\test.jpg", 'jpeg')