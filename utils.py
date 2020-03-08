import os
import cv2
import pytesseract
from PIL import Image

data_dir = os.getcwd() + "/data/"

def read_image(filename):
    img = cv2.imread(data_dir + filename,0)
    ret, thresh = cv2.threshold(img, 10, 255, cv2.THRESH_OTSU)
    cv2.imwrite(data_dir + "thresh_" + filename, thresh)
    text = pytesseract.image_to_string(Image.open(data_dir + "thresh_" + filename))
    return text