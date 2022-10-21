import os
import re
import json
import textract

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
        regex_school_district = re.compile("[a-zA-Z0-9 ]*\sSD\s[a-zA-Z0-9]*")
        #regex_phone = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")

        # first flag
        fst_flag = False

        aggblock = []
        principals = {}
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
                # when we match the next SD school district
                # reset the blocks
                currentblock = ""
                fst_flag = True
                currentblock = match_sd.group(0)
                principals[currentblock] = {"mails":{},"names":{}}

                if len(principals.keys()) >= 20:
                    break

            if fst_flag:
                if 'Principal' in line:
                    blockname = lines[i+1].strip()
                    
                if '@' in line:
                    blockmail = line.strip()

                aggblock.append(line.strip())

            if line == "\n" and fst_flag:
                if blockname:
                    principals[currentblock]["names"][blockname] = aggblock
                    blockname = ""
                    
                if blockmail:
                    principals[currentblock]["mails"][blockmail] = aggblock
                    blockmail = ""

                aggblock = []

        # define functions to use
        # function . 
        # funcs = [
        #     lambda n: ".".join(n).lower(),
        #     lambda n: (n[0][0]+n[1]).lower(),
        #     lambda n: (n[0]+n[1][0]).lower()
        # ]

        namesEmails = {k: {} for k in principals.keys()}
        
        # for each school district
        for sd,nm in principals.items():
            names = nm["names"].keys()
            mails = nm["mails"].keys()
            # for each name
            for name in names:
                # split on whitespace
                ns = name.split()
                # for each set of name fragments
                # create email signatures
                emailsigs = [".".join(ns).lower()]

                if len(ns) > 1:
                    emailsigs.append((ns[0][0]+ns[1]).lower())
                    emailsigs.append((ns[0]+ns[1][0]).lower())
                    
                # match them
                matches = [mail for mail in mails for sig in emailsigs if sig in mail]
                if len(matches) > 0:
                    namesEmails[sd][name] = {"emails":matches,
                                             "phones":[nm["mails"][mail][:2] for mail in matches],}
                    
                
                    
                
        print(principals)
        print(namesEmails)
        print(len(namesEmails))

        print(json.dumps(namesEmails,indent=2))
           

                
            
if __name__ == "__main__":
    filepath= os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List.pdf")
    outpath = os.path.expanduser("~/projects/datasets/Oregon_Department_of_Education_School_List_textract_out.txt")
    getData(outpath)


    
