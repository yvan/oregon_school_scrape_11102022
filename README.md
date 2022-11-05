# intro

the basic issue with pdf scraping is that the data is structured visually in a way that the underlying data is not. there are different solutions to solve this. 


# method

- use textract to generate the text data stream [textract](textract.readthedocs.io/)
- then use regex to look for certain patterns to divide thise stream into blocks
- connect blocks together that may share data (name + email), blocks located close to each other in the stream
- search the blocks for connected data and produce a final structure

other resources:

https://betterprogramming.pub/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f

https://tabula-py.readthedocs.io/en/latest

https://textract.readthedocs.io/en/stable

https://github.com/py-pdf/PyPDF2

https://www.nltk.org/

