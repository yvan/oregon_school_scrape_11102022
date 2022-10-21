"""
i think maybe this is not that great... we should try to use textract
a lot of the data ends up stuck together in bad spots like institution ids
and phone numbers which cannot always be easily separated.
"""
import os
import PyPDF2
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


if __name__ == "__main__":
    filename = os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List.pdf")
    pdf = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf)
    count = 0
    num_pages = pdfReader.numPages
    text = [""] * num_pages
    while count < num_pages:
        page = pdfReader.getPage(count)
        text[count] += f"\n&--PAGESTART:{count}--&\n"
        text[count] += page.extractText()
        text[count] += f"\n&--PAGEEND:{count}--&\n"
        count += 1

    # if text == "":
    #     text = textract.process(fileurl, method='tesseract', language='eng')
    pdf.close()
    
    # now search the text for lines with the word "principal"
    # from page 13 onward, earlier pages have the word,
    # but they don't seem to be school principals
    # rather executive managers
    for page in text[12:]:
        page = page.split("\n")
        # try to create datablocks
        # which have schoolanem
        # i think the way to do it
        # is to look for institution
        # id but then take one
        # step behind to start the block
        # which includes the nae of the school
        # they all seem to end with email
        # which is the only thing which should
        # have an @ symbol...so let's try it

        # might want to lowercase the text data...
        maxblocks = 0
        blockstart = 0
        blockend = 0
        for i,line in enumerate(page):
            if "Institution ID:" in line:
                blockstart = i-1
            if "@" in line:
                blockend = i+1
                block = page[blockstart:blockend]
                print("block")
                print(blockstart, blockend)
                print(block)
                blockstart = blockend
                blockend = blockend
            if maxblocks == 50:
                break
            
            maxblocks += 1
        break
    
    # outfile = os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List_out.txt")
    # with open(outfile, "w") as f:
    #     f.write(text)
    #     f.close()




