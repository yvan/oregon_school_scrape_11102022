



# issue with essy pdfs

problem 1 emails don't match names.
problem 2 some names are split on 2 lines
and so we only get one part (like Byron) of the name

what i could do is to match names and emails somehow like in a soup.
i could rank the emails by likelihood of beloning to the person.


the problem is block data is split up by principal name and email,
they are coming in separate blocks.

GRADES PRINCIPAL AND SCHOOL ALL FOLLOW EACH OTHER
BUT EMAILS NO. THEY ARE IN A DIFFERENT COLUMN
THE DATA IS READ AS COLUMNS BY PAGE SO WE COULD JUST TRY MATCHING INDICES
BY PAGE
OR WE COULD TAKE some window around the principal data and look for email by string matching.
OR BOTH INDICES TO REDUCE SEARCH AREA, STRING MATCHING TO CONFIRM.
this is probably a typical pattern in pdfs.

but how to know when we've passed to a new column?? the extraction algo would know.
but the data is not given i nthe byte stream or elsewhere. see a library with that
kind of structured info would be very useful page limits, sides and bottoms.
most have a FAX number at the top which we could regex...
if we match the regex... for a phone number... we can then assume the start of the 3rd column? might owrk.


OK institution id and principal data (the first 2 columns) actually come together. then phone numbers come after
so what we can do is... build an number of indices -+2 for the last emails and then when the regex match hits


start at _ SD _OR institution id
build index pausing counting when we hit 2 linefeeds 
hit phone number regex
check indices in window,
string match names to emails,
end at last email
restart at next institution id.

so the scanner reads the SD then it reads the left part of the the first block, then the right, then left then right all the way down. then it reads the phone numbers as a separate column/block all the way down.

the difference between "blocks" or within blocks seems to be 3 blank lines. ok it's actually 2 linefeeds in a row.

i cannot seem to get teh regex to detect 2 linefeeds in a row to work... you should be able to just copy some pattern prtined and then it generates some regex or code to capture it. the problem is not interesting b ut it is a pain and a common painpoint.

no but... it IS a line as all i'm doing is printing the test lines...

ok i'm a bit tired of all of this. the structure in the pdf is too unreliable. it does not break nicely into columns

i'm going to grab every name and split it on whitespace, put it in a dict.
grab every email and split it on @ and .

then toss all those things into a dict. (the emails have to connect to the phone numbers so we still want the blocks).

then once we match a name and email via the dict, pull out also the phone numbers from maybe a separate dict.

the pattern is

Name:

Roland Hobson

Email:

roland.hobson@BLA

rhobson@BLA
hobsonr@BLA

rolandh@BLA
hroland@BLA

ok



ok a neasier way would be...
we have soem current block
it builds when it hits the SD match
it appends into the overall block when we hit a linefeed.

https://betterprogramming.pub/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
https://github.com/py-pdf/PyPDF2
https://textract.readthedocs.io/en/stable
https://tabula-py.readthedocs.io/en/latest
https://www.nltk.org/
