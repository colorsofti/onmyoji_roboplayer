# coding=utf-8


import pytesseract
from PIL import Image

image = Image.open("pictures\\mark\\original_ui\\explore\\button_main_menu_explorer.jpg")
image.load()
code = pytesseract.image_to_string(image, lang='chi_sim').decode('utf8')
print (code)