# from PIL import Image
# # from pytesseract import *
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'

# image01 = Image.open("FLIR_20211007_095513.jpg")

# Print01 = pytesseract.image_to_string(image01, config='--psm 6')

# print(Print01)



######

from PIL import Image
from PIL import ImageGrab
# from pytesseract import *
import pytesseract
import re
import cv2
import numpy as np
import time
import os
import glob

pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'

path = glob.glob("C:/Users/star/Documents/test/*.jpg")
temp = 0
file = open('temp_out.txt', 'w')
for img in path:
    # image = cv2.imread("FLIR_20211007_105711.jpg")
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # write the grayscale image to disk as a temporary file so we can
    # 글자 프로세싱을 위해 Gray 이미지 임시파일 형태로 저장.
    filename = "{}.jpg".format(os.getpid())
    cv2.imwrite(filename, gray)

    # Simple image to string
    text = pytesseract.image_to_string(Image.open(filename), lang=None)
    os.remove(filename)

    
    temp = text.split()
    # if "°C" in temp[len(temp)-2]:
    if "°C" in temp[0]:         
        numbers = re.sub(r'[^0-9]', '', temp[0])
            
        file.write(numbers)
        file.write("\n")
            # print(numbers)
    
    # print(text.split()[0])
file.close()     

# cv2.imshow("Image", image)
# cv2.waitKey(0)