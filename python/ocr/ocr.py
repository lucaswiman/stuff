from wand.image import Image as wand_Image
from PIL import Image as PIL_Image
from wand.color import Color
import os
import pytesseract

def build_images(force=False):
    if not all([not force, os.path.isfile('./foo-0.png'), os.path.isfile('./foo-0.png')]):
        all_pages = wand_Image(filename='./example.pdf', resolution=300)
        for idx, page in enumerate(all_pages.sequence):
            with Image(page) as i:
                i.format = 'png'
                i.background_color = Color('white')
                i.alpha_channel = 'remove'
                i.save(filename='foo-%s.png' % idx)


build_images()

boxes = pytesseract.image_to_boxes(PIL_Image.open('foo-0.png'), output_type=pytesseract.Output.DICT)
data = pytesseract.image_to_data(PIL_Image.open('foo-0.png'), output_type=pytesseract.Output.DICT)
osd = pytesseract.image_to_osd(PIL_Image.open('foo-0.png'), output_type=pytesseract.Output.DICT)
