import os
import urllib2
from BeautifulSoup import BeautifulSoup
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

apiPrefix = 'tzuhua'
tzhpUrl = 'http://www.tzuchi.com.tw/tzuchi/Family/Default.aspx?AppSiteID=1'

# ------------------------------------------------------------
class HelloWorld(webapp.RequestHandler):
    def get(self):
        self.response.out.write("HELLO WORLD")

class DepartmentParser(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Req for department list ...")

class DoctorParser(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Req for doctor list ...")

# ------------------------------------------------------------

ROUTES = [
    ('/' + apiPrefix + '/dept', DepartmentParser),
    ('/' + apiPrefix + '/doctor', DoctorParser),
    ('/', HelloWorld),
]
application = webapp.WSGIApplication( ROUTES, debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
