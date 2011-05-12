# -*- coding: utf-8 -*-
import os
import re
import urllib
import urllib2
import datetime
import cookielib
from BeautifulSoup import BeautifulSoup
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Department, Doctor, Clinic, Register
from models import SUPPER_DPT

apiPrefix = 'tzuhua'

tzuUrl = 'http://www.tzuchi.com.tw/tzuchi/Family/'
dptUrl = 'http://www.tzuchi.com.tw/tchw/opdreg/SecList_HL.aspx'
tzuPrifix = 'http://www.tzuchi.com.tw/tchw/opdreg/'
cancelUrl = 'http://www.tzuchi.com.tw/tchw/opdreg/RegQryCancel.aspx?Loc=0'

# -------------------------------------------------------------------
class DepartmentReloader(webapp.RequestHandler):
    def get(self):
        return

class DepartmentRemover(webapp.RequestHandler):
    def get(self):
        depts = Department.all()
        for one in depts:
            one.delete()
        return	

class DepartmentParser(webapp.RequestHandler):
    def get(self):
        soup  = BeautifulSoup( urllib2.urlopen( dptUrl ) )
        table = soup.form.find('table', id='Table1')
        tdlist = table.findAll('td')
        
        code = 0;
        for td in tdlist:
            name = td.a.text.split('(')[0]    # Using split to escape the spcial case
            dpt = Department()
            dpt.dptName = name          # Removing the @ character 
            dpt.dptCode = code
            code = code + 1

            urlStr1 = 'http://www.tzuchi.com.tw/tchw/opdreg/OpdTimeShow.aspx?Depart='
            urlStr2 = '&HospLoc=3'
            dpt.dptLink = urlStr1 + urllib2.quote(name.encode('utf-8')) + urlStr2
            dpt.put()
        
        return

# -------------------------------------------------------------------
class DoctorReloader(webapp.RequestHandler):
    def get(self):
        return

class DoctorRemover(webapp.RequestHandler):
    def get(self):
        return

class DoctorParser(webapp.RequestHandler):
    def get(self):
        return

# --------------------------------------------------------------------
class ClinicReloader(webapp.RequestHandler):
    def get(self):
        return

class ClinicRemover(webapp.RequestHandler):
    def get(self):
        return

class ClinicParser(webapp.RequestHandler):
    def get(self):
        return

# --------------------------------------------------------------------

ROUTES = [
    ('/cjobs/clinic/reload', ClinicReloader),
    ('/cjobs/clinic/remove', ClinicRemover),
    ('/cjobs/clinic/parser', ClinicParser),
    ('/cjobs/doctor/reload', DoctorReloader),
    ('/cjobs/doctor/remove', DoctorRemover),
    ('/cjobs/doctor/parser', DoctorParser),
    ('/cjobs/dept/reload', DepartmentReloader),
    ('/cjobs/dept/remove', DepartmentRemover),
    ('/cjobs/dept/parser', DepartmentParser),
]

application = webapp.WSGIApplication( ROUTES, debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
