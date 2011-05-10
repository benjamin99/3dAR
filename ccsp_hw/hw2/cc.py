# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup

url = 'http://www.tzuchi.com.tw/tchw/opdreg/RegQryCancel.aspx?Loc=0'

vals = {}
vals['RadioButtonList1'] = '花蓮'
vals['txtMRNo'] = 'A123123123'
vals['btnQry'] = '查詢'
vals['__EVENTARGUEMENT'] = ''
vals['__EVENTTARGET'] = ''
vals['__VIEWSTATE'] = ''

cookie = cookielib.CookieJar()
hth    = urllib2.HTTPHandler( debuglevel=1 )
hsh    = urllib2.HTTPSHandler( debuglevel=1 )

opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookie), hth, hsh)

print 'Operation: GET ----------------------'
req = urllib2.Request(url)
rsp = opener.open(req)
soup = BeautifulSoup(rsp)

qText = soup.find(id='lblQuestion').text
print qText
if len(qText.split('+')) == 2:
    A = qText.split('+')[0]
    B = qText.split('+')[1].split('=')[0]
    C = int(A) + int(B)
    print C

elif len(qText.split('-')) == 2:
    A = qText.split('-')[0]
    B = qText.split('-')[1].split('=')[0]
    C = int(A) - int(B)
    print C

vals['txtAnswer'] = str(C)
vals['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']
vals['__VIEWSTATE'] = soup.form.find(id='__VIEWSTATE')['value']

print 'Operation: POST --------------------'
req = urllib2.Request(url, urllib.urlencode(vals) )
rsp = opener.open(req)

soup = BeautifulSoup(rsp)
error = soup.find(id='Label5')
if error: # No Registeration
    print error.text

else:    
    rTable = soup.find(id='dgList')
    results = rTable.findAll('tr')
    row = 0
    for one in results:
        if row != 0:
            print one.find('a')['href']
        row = row + 1
