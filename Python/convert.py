import textract
import os
import textwrap

#TODO Add a last page you fucking fool

def main():
    pdfDir = '/home/pi/Books/PDF' #'/home/henry/Books/PDF'
    txtDir = '/home/pi/Books/TXT' #'/home/henry/Books/TXT'

    pdfs = []

    for r, d, f in os.walk(pdfDir):
        for file in f:
            if '.pdf' in file:
                pdfs.append(os.path.join(r, file))
    
    for i in range(len(pdfs)):
        name = pdfs[i].replace(pdfDir + '/', '')
        name = name.replace('.pdf', '')
        print(str(i) + ') ' + name)

    selected = pdfs[int(input("Convert: "))]
    name = selected.replace(pdfDir + '/', '')
    name = name.replace('.pdf', '')
    
    txtFile = txtDir + '/' + name + '.txt'

    if (os.path.exists(txtFile)):
        if (raw_input("Text file for " + name + " already exists.\nDo you want to overwrite it? (yes/no)\n: ") == "yes"):
            convertToTXT(txtFile, selected)
    else:
        convertToTXT(txtFile, selected)

def convertToTXT(txtFile, selected):

    lineWidth = 37
    linesPerPage = 18
    lines = 0
    chapters = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN"]
    chapter = 0
    part = 1
    pageNumber = 1

    print("Converting PDF to txt file")
    if (os.path.exists(txtFile)):
        txtFile = open(txtFile, 'w+')
    else:
        txtFile = open(txtFile, 'w+')

    text = str(textract.process(selected))
    
    text = text.replace("\n", " ")
    text = text.replace("\f", "")

    txtFile.write("\f1,0,1\n")

    for line in textwrap.wrap(text, width = lineWidth):
        if (line.find(chapters[chapter]) != -1):
            line = line.replace(chapters[chapter], "\n\f" + str(part) + "," + str(chapter) + "," + str(pageNumber) + "\n" + chapters[chapter] + "\n")
            chapter += 1
            pageNumber = 1
            lines = 2
        elif(line.find(chapters[0]) != -1):
            chapter = 0
            line = line.replace(chapters[chapter], "\n\f" + str(part) + "," + str(chapter) + "," + str(pageNumber) + "\n" + chapters[chapter] + "\n")
            pageNumber = 1
            chapter = 1
            part += 1
            lines = 2
        txtFile.write(line)
        if (lines < linesPerPage):
            txtFile.write("\n")
            lines += 1
        else:
            txtFile.write("\n\f" + str(part) + "," + str(chapter) + "," + str(pageNumber) + "\n")
            lines = 1
            pageNumber += 1
    
    txtFile.write("\n\f" + str(part) + "," + str(chapter) + "," + str(pageNumber))


main()

