usb_codes = {
    "04":"aA", "05":"bB", "06":"cC", "07":"dD", "08":"eE", "09":"fF",
    "0a":"gG", "0b":"hH", "0c":"iI", "0d":"jJ", "0e":"kK", "0f":"lL",
    "10":"mM", "11":"nN", "12":"oO", "13":"pP", "14":"qQ", "15":"rR",
    "16":"sS", "17":"tT", "18":"uU", "19":"vV", "1a":"wW", "1b":"xX",
    "1c":"yY", "1d":"zZ", "1e":"1!", "1f":"2@", "20":"3#", "21":"4$",
    "22":"5%", "23":"6^", "24":"7&", "25":"8*", "26":"9(", "27":"0)",
    "2c":"  ", "2d":"-_", "2e":"=+", "2f":"[{", "30":"]}",  "32":"#~",
    "33":";:", "34":"'\"",  "36":",<",  "37":".>"
    }
f=open("leftover2.txt").read()
f=f.split("\n")
li=[0]
for i in f:
    if "00" == i[:2] or "02" == i[:2] or "01" == i[:2]: # "00" for non-shift |  "01" for ctrl+ | "02" for shift 
        if "0"*10 in i:
            if li[-1]!=i:
                li.append(i)


lines = ["","","","","","","","",""]  #to handle 
        
pos = 0

for i in li[1:]:
    if i[4:6]=="51" or i[4:6]=="28":
        pos+=1
        continue
    elif i[4:6]=="52":
        pos-=1
        continue
    if "0000000000" in i:
        try:
            if i[:2]=="01":
                print(lines)
            if i[:2]=="02":
                lines[pos]+=usb_codes[i[4:6]][1] 
            elif i[:2]=="00":
                lines[pos]+=usb_codes[i[4:6]][0]
        except:
            pass

print(lines)
