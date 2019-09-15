# -*- coding: utf-8 -*-
import epd7in5
import textwrap
import PyPDF2
import textract
from PIL import Image, ImageDraw, ImageFont

def main():

    lineWidth = 37
    fontSize = 16
    lineSpacing = 18
    fontPath = '/home/pi/.fonts/AnonymousPro-Regular.ttf'
    pdfPath = '/home/pi/test.pdf'

    epd = epd7in5.EPD()
    epd.init()

    size = epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT

    image = Image.new('1', (epd7in5.EPD_HEIGHT, epd7in5.EPD_WIDTH), 255)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(fontPath, fontSize)

    margin = offset = 10

    text = textract.process(pdfPath)

    text = text.replace('‘', '\'')
    text = text.replace('’', '\'')

    for line in textwrap.wrap(text, width = lineWidth):
        print(line)
        draw.text((margin,offset), line, font=font)
        offset += lineSpacing

    new_image = image.rotate(180)

    epd.display(epd.getbuffer(new_image))

if __name__ == '__main__':
    main()