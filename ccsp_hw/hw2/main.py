import os
import urllib2
from BeautifulSoup import BeautifulSoup
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Department
from models import SUPPER_DPT

apiPrefix = 'tzuhua'
dptUrl = 'http://www.tzuchi.com.tw/tzuchi/Family/Default.aspx?AppSiteID=1'

# ------------------------------------------------------------
class HelloWorld(webapp.RequestHandler):
    def get(self):
        self.response.out.write("HELLO WORLD")

class DepartmentParser(webapp.RequestHandler):
    def get(self):
        soup  = BeautifulSoup( urllib2.urlopen(dptUrl) )
        form  = soup.find('form', id = 'Form1' )
        table = form.contents[25].findAll('table')
  
        for i in range(0, len(table) ):
            subDptList = table[i].findAll('a')
            j = 0
            for one in subDptList:
                j = j + 1
                dept = Department()
                dept.dptName = one.text
                dept.dptCode = (i+1)*100 + j
                if i < 4:
                    dept.supper  = SUPPER_DPT[i]  
                dept.put()
        
        self.response.out.write("Finish for department list ...")

class DepartmentFetcher(webapp.RequestHandler):
    def get(self):
        dptList = Department.all() #.order('dptCode')
        for one in dptList:
            self.response.out.write('%s' % one.dptName ) 
            self.response.out.write(' %d\n' % one.dptCode )       

class DoctorParser(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Req for doctor list ...")

# ------------------------------------------------------------

ROUTES = [
    ('/' + apiPrefix + '/dept/parse', DepartmentParser),
    ('/' + apiPrefix + '/doctor/parse', DoctorParser),
    ('/' + apiPrefix + '/dept', DepartmentFetcher ),
    #('/' + apiPrefix + '/doctor', DoctorFetcher)
    ('/', HelloWorld),
]
application = webapp.WSGIApplication( ROUTES, debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
