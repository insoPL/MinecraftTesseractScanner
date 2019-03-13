# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
import pytesseract
import re
import pyscreeze


class Scanner(QThread):
    refresh = pyqtSignal()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

    def __init__(self):
        QThread.__init__(self)
        self.rotate = float(0)
        self.x = float(0)
        self.z = float(0)

    def run(self):
        while True:
            screenshot = pyscreeze.screenshot()
            #screenshot = Image.open("screenshot.png")
            try:
                cropped_screenshot = screenshot.crop((380, 325, 800, 358))  # crop screenshot
                text = pytesseract.image_to_string(cropped_screenshot)  # send image to tesseract for OCR
                text = re.search("\((.*)\)", text).group()  # delete some not important characters
                text = text[1:-1]  # more of the same
                angle, pitch = text.split('/')  # split angle and pitch
                self.rotate = float(angle)  # and turn it into float

                cropped_screenshot = screenshot.crop((65, 245, 700, 275))  # now do same thing with cords
                text = pytesseract.image_to_string(cropped_screenshot)
                x, y, z = text.split('/')
                self.x = float(x)
                self.z = float(z)

                self.refresh.emit()  # inform  main window about new data to show
            except:
                # broad exception but there is a lot things that can fail
                # Failed or not it's not detrimental for program stability
                # Test showed about 20% fail ratio. It depends on font, light, background etc
                continue

    def __del__(self):
        self.quit()
        self.wait()
