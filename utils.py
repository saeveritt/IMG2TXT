import os
import cv2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path




class Utils():
    def __init__(self, filename):
        self.data_dir = os.getcwd() + "/data/"
        self.ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif']
        self.filename = filename.strip()
        self.filetype = self.file_type()
        self.isPDF = self.filetype == "pdf"
        self.newfile = ''
    def read_image(self):
        self.filetype = self.file_type()
        if self.filetype == "pdf":
            return self.convertPDF()
        else:
            return self.find_text()

    def find_text(self,new=False):
        img = cv2.imread(self.data_dir + self.filename,0)
        ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO)
        filename = self.filename
        if new:
            filename = self.newfile
        print(self.data_dir + "thresh_" + filename)
        cv2.imwrite(self.data_dir + "thresh_" + filename, thresh)
        text = pytesseract.image_to_string(Image.open(self.data_dir + "thresh_" + filename))
        return text

    def allowed_file(self):
        check = self.filetype in self.ALLOWED_EXTENSIONS
        return check

    def file_type(self):
        return self.filename.rsplit('.', 1)[1].lower()

    def convertPDF(self):
        text = ""
        pages = convert_from_path(self.data_dir + self.filename,300)
        newfile = self.filename[:-4] + '.jpg'
        for i,page in enumerate(pages):
            self.newfile = str(i) +"_"+ newfile
            print(page)
            page.save(self.newfile, 'JPEG')
            text += self.find_text(new=True) + "\n"
        return text
