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
        # get the lines from the pdf
        lines = [line.decode('utf-8') for line in f]

        # compile a regex for detecting each school district
        regex_school_district = re.compile("[a-zA-Z0-9 ]*\sSD[\sa-zA-Z0-9]*")

        # this section collects data into a dictionary, called principals
        # basically it organized the data by the names of the principals
        # so we can limit our search later to look within a particular block
        # i.e. from one _SD_ match to another
        principals = OrderedDict()                
        fst_flag = False
        currentblock = ""
        blockname = ""
        blockmail = ""
        aggblock = []
        
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
                
        # add previous and next blocks to the
        # data because it's a bit scrambled
        windowidx = 1
        previous = []
        keys = list(principals.keys())
        for i,key in enumerate(keys):
            principals[key]['previous'] = previous.copy()
            principals[key]['next'] = keys[i+1:i+3]
            if i > windowidx:
                previous.pop(0)
            previous.append(key)
            
        # in this section build a dictionary
        # of names and emails for every school
        # district
        namesEmails = {k: {} for k in principals.keys()}
        
        # for each school district
        for sd,nm in principals.items():
            # add values from prior/next
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

                # remove anything which is 1 or 2 letters
                ns = [n for n in ns if len(n)>2]
                
                # for each set of name fragments
                # create email signatures
                emailsigs = [".".join(ns).lower()]

                if len(ns) > 1:
                    emailsigs.append((ns[0][0]+ns[1]).lower())
                    emailsigs.append((ns[0]+ns[1][0]).lower())
                    emailsigs.append((ns[1]).lower())
                    
                # match them
                matches = [mail for mail,emailsig in product(mails,emailsigs) if emailsig in mail.split("@")[0]]
                
                #matches = [mail for mail in mails for sig in emailsigs if sig in mail]
                if len(matches) > 0:
                    namesEmails[sd][name] = {"district":sd,
                                             "emails":matches,
                                             "phones":[nm["mails"][mail][:2] for mail in matches],}
                    

        # print info about data
        print(json.dumps(namesEmails,indent=2))
        print("entries")
        print(len(namesEmails))
        print("entries with more than 0 thing")
        print(len([1 for v in namesEmails.values() if len(v) > 0]))

        # save to a file
        with open("output.json", 'w') as f:
            json.dump(namesEmails,f,indent=2)
                
            
if __name__ == "__main__":
    filepath= os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List.pdf")
    outpath = os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List_textract_out.txt")
    getData(outpath)


    
