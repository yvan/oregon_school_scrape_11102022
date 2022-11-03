"""
-first understand how the stream of data comes out from textract or py2pdf or tabula-py
-second produce an index of this data stream, preferably in one or two passes, the index
is like an object, database or set of relations that connects the data intelligently,
for example by section, visually, and then drawing connections between "adjacent" sections,
or something that can reliably map names and emails together.
-third use the index to construct a final dataset with names, emails, numbers, whatever
the client is looking for
- four quality control, check a sample of the output for quality, flaws, etc.
- five get early client feedback on data quality, iterate and improve.
- one thing is that when someone has a short name like "thao do," since
  do appears in a bunch of other words it has a huge hit rate.
- another thing is hits from someone's name like "will" to the name of a district
  like willamina.
- another thing to realize is that school, not district
  determines the email address.

daloopa
"""

import os
import re
import json
import textract
from itertools import product
from collections import OrderedDict

def numNameMatch(name, email):
    names = name.split()
    return sum([1 for n in names if n.lower() in email.lower()])

def getPdfText(inpath,outpath):        
    text = textract.process(inpath)
    with open(outpath, "wb") as f:
        f.write(text)

def getData(textfile):
    with open(textfile, 'rb') as f:
        lines = [line.decode('utf-8') for line in f]
        regex_school_district = re.compile("[a-zA-Z0-9 ]*\sSD[\sa-zA-Z0-9]*")
        #regex_phone = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")

        # first flag
        fst_flag = False

        testflag = False

        aggblock = []
        principals = OrderedDict()
        previousblock = ""
        currentblock = ""
        blockname = ""
        blockmail = ""

        # this section collects data into a dictionary, called principals
        # basically it organized the data by the names of the principals
        # so we can limit our search later to look within a particular block
        # i.e. from one _SD_ match to another
        
        for i,line in enumerate(lines):         
            match_sd = re.search(regex_school_district, line)
            
            if match_sd:
                currentblock = ""
                fst_flag = True
                currentblock = match_sd.group(0).strip()
                if principals.get(currentblock) is None:
                    principals[currentblock] = {"mails":{},"names":{}}

            if fst_flag:
                if 'Principal' in line:
                    blockname = lines[i+1].strip()
                    
                if '@' in line:
                    blockmail = line.strip()

                aggblock.append(line.strip())

            if line == "\n" and fst_flag:                
                if blockname:
                    principals[currentblock]["names"][blockname] = aggblock.copy()
                    blockname = ""
                    
                if blockmail:
                    principals[currentblock]["mails"][blockmail] = aggblock.copy()
                    blockmail = ""

                aggblock = []
                
        # create previous mappings
        windowidx = 1
        previous = []
        keys = list(principals.keys())
        for i,key in enumerate(keys):
            principals[key]['previous'] = previous.copy()
            principals[key]['next'] = keys[i+1:i+3]
            if i > windowidx:
                previous.pop(0)
            previous.append(key)
            

        namesEmails = {k: {} for k in principals.keys()}
        
        # for each school district
        for sd,nm in principals.items():
            # add values from prior
            # and next
            for nextprev in nm['previous'] + nm['next']:
                for name, blockvalues in principals[nextprev]['names'].items():
                    if nm['names'].get(name) is None:
                        nm['names'][name] = blockvalues
                for mail, blockvalues in principals[nextprev]['mails'].items():
                    if nm['mails'].get(mail) is None:
                        nm['mails'][mail] = blockvalues                  
            
            names = list(nm["names"].keys())
            mails = list(nm["mails"].keys())
            
            for name in names:
                # split on whitespace
                ns = name.split()
                # for each set of name fragments
                # create email signatures
                emailsigs = [".".join(ns).lower()]

                if len(ns) > 1:
                    emailsigs.append((ns[0][0]+ns[1]).lower())
                    emailsigs.append((ns[0]+ns[1][0]).lower())
                    emailsigs.append((ns[1]).lower())
                    
                # match them
                matches = [mail for mail,emailsig in product(mails,emailsigs) if emailsig in mail]
                print(sd)
                print(len(matches))
                print()
                #matches = [mail for mail in mails for sig in emailsigs if sig in mail]
                if len(matches) > 0:
                    namesEmails[sd][name] = {"district":sd,
                                             "emails":matches,
                                             "phones":[nm["mails"][mail][:2] for mail in matches],}
                    
        
        # print(principals)
        # print(namesEmails)
        print(json.dumps(namesEmails,indent=2))
        print("entries")
        print(len(namesEmails))
        print("entries with more than 0 thing")
        print(len([1 for v in namesEmails.values() if len(v) > 0]))
           

        """
        the SD is not a good separator because sometimes (for reasons i don't understand)
        it reads the next one before the email section of the SD you'r currently on.

        that means we need a bit of a different strategy, instead of seaching inside one "SD"
        we can maybe search a window?? dunno.

        could just try the simple thing to include... previous block and next block??
        """
                
            
if __name__ == "__main__":
    filepath= os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List.pdf")
    outpath = os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List_textract_out.txt")
    getData(outpath)


    
