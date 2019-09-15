import epd7in5
import os
from PIL import Image, ImageDraw, ImageFont

def main():

    lineWidth = 37
    fontSize = 16
    lineSpacing = 18
    linesPerPage = 18

    bookDir = "/home/pi/Books/TXT"
    fontPath = "/home/pi/.fonts/AnonymousPro-Regular.ttf"

    epd = epd7in5.EPD()
    epd.init()
    size = epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT
    image = Image.new('1', (epd7in5.EPD_HEIGHT, epd7in5.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(fontPath, fontSize)

    margin = offset = 10

    books = []

    for r, d, f in os.walk(bookDir):
        for file in f:
            if '.txt' in file:
                books.append(os.path.join(r, file))

    book = open(books[0], "r")
    booklines = book.readlines()

    bookmark = booklines[0]

    for i in range(len(booklines)):
        if (booklines[i] == bookmark):
            pageIndex = i

    pageStop = False
    counter = 1

    while (pageStop == False):
        if ("\f" in booklines[pageIndex - counter]):
            printLines = counter
            pageStop = True
        else:
            counter += 1
    
    for x in range(printLines - 1):
        draw.text((margin, offset), booklines[pageIndex - (printLines - x) + 1], font=font)
        print(booklines[pageIndex - (printLines - x) + 1])
        offset += lineSpacing

    epd.display(epd.getbuffer(image))

    book.close()



main()

# 1. Open converted books folder and display the books
# 2. Ask the user which book they want to read
# 3. Find the current page by opening the bookmark file
# 4. Display the lines on the current page
# 5. Upon a button press, go to the next page by looking for the /f
# 6. Set the new bookmark