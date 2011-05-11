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
            #script =  one.find('a')['href']
            tds = one.findAll('td')
            col = 0
            for td in tds:
                if col == 0:
                    script = td.find('a')['href']
                elif col == 1:
                    date = td.text
                elif col == 2:
                    time = td.text
                elif col == 4:
                    docName = td.text
                col = col + 1
            
            year  = str(int(date[:3]) + 1911)
            month = date[3:5]
            day   = date[5:]

            if time == u'早上':
                time = 'A'
            elif time == u'下午':
                time = 'B'
            elif time == u'晚上':
                time = 'C'
            
            datetime = year + '-' + month + '-' + day + '-' + time
            target = script.split('\'')[1].split('\'')[0]
            print datetime
            print docName
            print script
            print target

        row = row + 1
    
    vals['__EVENTTARGET'] = target
    vals['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']
    vals['__VIEWSTATE'] = soup.form.find(id='__VIEWSTATE')['value'] 
    del vals['btnQry']

    req = urllib2.Request(url, urllib.urlencode(vals) )
    rsp = opener.open(req)
    soup = BeautifulSoup( rsp )
    print soup


