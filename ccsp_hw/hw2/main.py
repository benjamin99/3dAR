import os
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Department, Doctor, Clinic
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
            dpt.dptName = name          # Removing the @ character 
            dpt.dptCode = code
            code = code + 1

            urlStr1 = 'http://www.tzuchi.com.tw/tchw/opdreg/OpdTimeShow.aspx?Depart='
            urlStr2 = '&HospLoc=3'
            dpt.dptLink = urlStr1 + urllib2.quote(name.encode('utf-8')) + urlStr2
            dpt.put()
        
        self.response.out.write("Finish for department list ...")

class DepartmentFetcher(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        jsArray = []

        if not id:
            dptList = Department.all() 
            for one in dptList:
                jsObj = { 
                    str(one.dptCode):one.dptName
                    #'link'          :one.dptLink  
                }
                jsArray.append( jsObj )
       
        else: 
            jsArray.append( {"id": id } )
            dept = Department.all().filter('dptCode = ', int(id) ).get()
            if dept:
                jsArray.append( {"name": dept.dptName } )
                
                # searching for the clinic info:
                doctors  = []
                docCodes = []
                clinics = Clinic.all().filter('dept =', dept.key() ).order('doctor')
                for one in clinics:
                    if one.doctor.docCode not in docCodes:
                        docCodes.append( one.doctor.docCode )
                        doctors.append( { one.doctor.docCode : one.doctor.docName } )

                jsArray.append( { "doctor" : doctors }) 
    
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( simplejson.dumps(jsArray) )

class DepartmentRemover(webapp.RequestHandler):
    def get(self):
        departments = Department.all()
        for one in departments:
            one.delete()

        self.response.out.write('Delete all department data ...')

class DoctorRemover(webapp.RequestHandler):
    def get(self):
        doctors = Doctor.all()
        for one in doctors:
            one.delete()
        self.response.out.write('Delete all doctor data ...')

class DoctorParser(webapp.RequestHandler):    # Should pass the link to the department page:
    def get(self):
        code = int(self.request.get('code', '0'))
        q = Department.gql('WHERE dptCode >= :1 ORDER BY dptCode', code)
        dpts = q.fetch(limit=2)
        nowDpt  = dpts[0]
        
        soup = BeautifulSoup( urllib2.urlopen( nowDpt.dptLink ) )
        list = soup.table.findAll('a')
        for one in list:
            text = one.text;
            name = re.split('[0-9]', text)[0]
            code = text[ len(name):].split(' ')[0].split('(')[0]  # Dealing w/ the special cases
            doc  = Doctor.all().filter('docCode =', code).get()
            if not doc and len(code) != 0:
                doc = Doctor()
                doc.docName = name
                doc.docCode = code
                doc.put()
        
        if( len(dpts) > 1):
            nextDpt  = dpts[1] 
            nextUrl  = '/parse/doctor?code=%d' %  nextDpt.dptCode 
            nextName = nextDpt.dptName
        else:
            nextUrl  = '/'
            nextName = 'END OF PARSING'

        context = { 
            'type'    : 'Doctor',
            'nextUrl' : nextUrl,
            'nextName': nextName,
        }
        path = os.path.join( os.path.dirname('__file__'), 'templates', 'parser.html')
        self.response.out.write( template.render( path, context) )

class DoctorFetcher(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        jsArray = [];

        if not id:
            docList = Doctor.all()
            for one in docList:
                jsObj = {
                        one.docCode: one.docName
                }
                jsArray.append( jsObj )
        
        else:
            jsArray.append( { "id": id } ) 
            doc = Doctor.all().filter('docCode =', id).get()
            if doc:
                jsArray.append( {"name": doc.docName } )

                # searching for the clinic info:
                depts = []
                deptCodes = [] 
                clinics = Clinic.all().filter( 'doctor =', doc.key() ).order('dept')
                for one in clinics:
                    if one.dept.dptCode not in deptCodes:    # making sure that dept will not be repeated
                        deptCodes.append( one.dept.dptCode )
                        depts.append( { one.dept.dptCode : one.dept.dptName } )
                
                jsArray.append( { "dept": depts } )
                 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( simplejson.dumps(jsArray) )

class ClinicRemover(webapp.RequestHandler):
    def get(self):
        clinics = Clinic.all()
        for one in clinics:
            one.delete()

        self.response.out.write('Removed all clinic data ...')

class ClinicParser(webapp.RequestHandler):
    def get(self):
        code = int(self.request.get('code', '0'))
        q = Department.gql('WHERE dptCode >= :1 ORDER BY dptCode', code)
        dpts = q.fetch(limit=2)
        nowDpt  = dpts[0]
        
        soup = BeautifulSoup( urllib2.urlopen( nowDpt.dptLink ) )
        list = soup.table.findAll( lambda tag: tag.name == 'a' and len(tag.attrs) == 2 )
        for one in list:
            text = one.text;
            name = re.split('[0-9]', text)[0]
            doc  = Doctor.all().filter('docName =', name).get()
            if doc:
                clinic = Clinic()
                link = one['href']
                code = link.split('data=')[1].split('&sLoc')[0]
                clinic.link   = link
                clinic.code   = code
                clinic.doctor = doc.key()
                clinic.dept   = nowDpt.key() 
                clinic.put()
        
        if( len(dpts) > 1):
            nextDpt = dpts[1]
            nextUrl  = '/parse/clinic?code=%d' %  nextDpt.dptCode 
            nextName = nextDpt.dptName
        else:
            nextUrl  = '/'
            nextName = 'END OF PARSING'

        context = { 
            'type'    : 'Clinic',
            'nextUrl' : nextUrl,
            'nextName': nextName,
        }
        path = os.path.join( os.path.dirname('__file__'), 'templates', 'parser.html')
        self.response.out.write( template.render( path, context) )

# ------------------------------------------------------------

ROUTES = [
    ('/remove/clinic', ClinicRemover),
    ('/remove/doctor', DoctorRemover),
    ('/remove/dept', DepartmentRemover),
    ('/parse/clinic', ClinicParser),
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
