           # matchlf_1 = re.search(regex_linefeed,line)
            # matchlf_2 = re.search(regex_linefeed,lines[i-1])
            # if matchlf_1 and matchlf_2:
            #     print("two linefeeds")
            
            
            # if incrementblock:
            #     block.append(line)
            
            
            # if "Principal" in line:
            #     principalName = lines[i+1].lower()
            #     principals[principalName] = {}
                
            
            if "Roland Hobson" in line:
                # for j in range(-10,10,1):
                testlines = lines[i-70:i+70]
                for l in testlines:
                    print(l)
                    print(l.encode("utf-8"))
                    matchlf_1 = re.search(regex_linefeed,line)
                    matchlf_2 = re.search(regex_linefeed,lines[i-1])
                    
                    check = "\n"
                    print("line check:", l, check, l == check)
                    if l == '\n':                
                        print("one linefeeds")
                        
                    # match_lf = re.search(regex_linefeed, line)
                    # if match_lf:
                    #     print("found linefeedq")
                    #print(l.encode('utf-8').hex())
                    regexphone = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")
                    match = re.search(regexphone, l)
                    # if match:



                   
            # if "rhobson@bakercharters.org" in line:
            #     # for j in range(-10,10,1):
            #     testlines = lines[i-70:i+70]
            #     for l in testlines:
            #         print(l)
                    # print(l.encode("utf-8"))
                    # matchlf_1 = re.search(regex_linefeed,line)
                    # matchlf_2 = re.search(regex_linefeed,lines[i-1])
                    
                    # check = "\n"
                    # print("line check:", l, check, l == check)
                    # if l == '\n':                
                    #     print("one linefeeds")
                        
                    # regexphone = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")
                    # match = re.search(regexphone, l)

                
            # # flag to record the second part of the first block (principal names)
            # if line == "\n" and fst_flag[0]:
            #     fst_flag[1] = True

            # # flag to record the second block (emails)
            # if line == "\n" and fst_flag[1]:
            #     fst_flag[2] = True

            # # # flag to record the final block.
            # # if line == "\n" and fst_flag[2]:
            # #     fst_flag[3] = True

            # whichBlock = sum(fst_flag)
            # if whichBlock == 1:
            #     block1.append(line)

            # elif whichBlock == 2:
            #     block2.append(line)

            # elif whichBlock == 3:
            #     block3.append(line)

            # elif whichBlock == 4:
            #     blocks.append((block1,block2,block3))
            #     block1 = []
            #     block2 = []
            #     block3 = []
            
        # for i,b in enumerate(blocks):
        #     print(b)
        #     if i == 20:
        #         break

                    
    # ok institution ID and 
                        
                        
                    
                    
            # if "Institution ID:" in line:
            #     # print(lines[i-1])
            #     # print(line)  
            #     block.append(lines[i-1])
            #     block.append(line)
            # if "@" in line:
            #     # print(line)
            #     block.append(lines[i-1])
            #     block.append(line)
            # if len(block) > 0:
            #     blocks.append(block)
        print(blocks)

        # principals = {}
        # for block in blocks:
        #     schoolid = None     
        #     for i,line in enumerate(block):
        #         if "Institution ID:" in line:
        #             schoolid = line.split(":")[1].rstrip()
        #             principals[schoolid] = {}
                    
        #         if schoolid and 'Principal' in line:
        #             principals[schoolid]["principal"] = block[i+1]
                    
        #         if schoolid and "@" in line:                    
        #             principals[schoolid]["email"] = line

        #         if principals.get(schoolid) and principals[schoolid].get('principal') and principals[schoolid].get('email'):
        #             print("name match")
        #             x = numNameMatch(principals[schoolid]["principal"], principals[schoolid]["email"])
        #             print(x)
        #             principals[schoolid]["nmatch"] = x
                
        # print(blocks)
