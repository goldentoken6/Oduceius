import os
import re
import pytesseract
from PIL import Image 
from pytesseract import pytesseract 
from pdf2image import convert_from_path
import preprocess

img_item_path = '1.jpg'

img = Image.open(img_item_path) 
text = pytesseract.image_to_string(img)

print(text)