import os
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Department, Doctor
from models import SUPPER_DPT

apiPrefix = 'tzuhua'

tzuUrl = 'http://www.tzuchi.com.tw/tzuchi/Family/'
dptUrl = 'http://www.tzuchi.com.tw/tchw/opdreg/SecList_HL.aspx'

# ------------------------------------------------------------
class HelloWorld(webapp.RequestHandler):
    def get(self):
        self.response.out.write("HELLO WORLD")

class DepartmentParser(webapp.RequestHandler):
    def get(self):
        soup  = BeautifulSoup( urllib2.urlopen( dptUrl ) )
        table = soup.form.find('table', id='Table1')
        tdlist = table.findAll('td')
        
        code = 0;
        for td in tdlist:
            name = td.a.text.split('(')[0]    # Using split to escape the spcial case
            dpt = Department()
            dpt.dptName = name 
            dpt.dptCode = code
            code = code + 1

            urlStr1 = 'http://www.tzuchi.com.tw/tchw/opdreg/OpdTimeShow.aspx?Depart='
            urlStr2 = '&HospLoc=3'
            dpt.dptLink = urlStr1 + urllib2.quote(name.encode('utf-8')) + urlStr2
            dpt.put()
        
        self.response.out.write("Finish for department list ...")

class DepartmentFetcher(webapp.RequestHandler):
    def get(self):
        dptList = Department.all() #.order('dptCode')
        jsList = [];
        for one in dptList:
            jsObj = { 
                      str(one.dptCode):one.dptName,
                      'link'          :one.dptLink  
                    }
            jsList.append( jsObj )
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( simplejson.dumps(jsList) )

class DoctorRemover(webapp.RequestHandler):
    def get(self):
        doctors = Doctor.all()
        for one in doctors:
            one.delete()
        self.response.out.write('Delete all doctor data ...')

class DoctorParser(webapp.RequestHandler):    # Should pass the link to the department page:
    def get(self):
#dptKey = self.request.get('key')
#        testStr = 'NOT OK'
#        if dptKey:
#            testStr = dptKey
#            dpt = db.get( dptKey )
        dptList = Department.all()
        for dpt in dptList:
            testStr = dpt.dptName
            soup = BeautifulSoup( urllib2.urlopen( dpt.dptLink ) )
            list = soup.table.findAll('a')
            for one in list:
                text = one.text;
                name = re.split('[0-9]', text)[0]
                code = text[ len(name):]
                doc  = Doctor.all().filter('docCode =', code).get()
                if not doc:
                    doc = Doctor()
                    doc.docName = name
                    doc.docCode = code
                    doc.put()

        self.response.out.write( testStr)

class DoctorFetcher(webapp.RequestHandler):
    def get(self):
        docList = Doctor.all() #.order('dptCode')
        jsList = [];
        for one in docList:
            jsObj = { 
                      'name': one.docName,
                      'code': one.docCode  
                    }
            jsList.append( jsObj )
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( simplejson.dumps(jsList) )

# ------------------------------------------------------------

ROUTES = [
    ('/remove/doctor', DoctorRemover),
    ('/parse/dept', DepartmentParser),
    ('/parse/doctor', DoctorParser),
    ('/' + apiPrefix + '/dept', DepartmentFetcher ),
    ('/' + apiPrefix + '/doctor', DoctorFetcher),
    ('/', HelloWorld),
]
application = webapp.WSGIApplication( ROUTES, debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
