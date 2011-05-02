from google.appengine.ext import db
from google.appengine.ext import blobstore

SUPPER_DPT = [ 'A', 'B', 'C', 'D']

class Department( db.Model ):
    dptName = db.StringProperty()
    dptCode = db.IntegerProperty()
    dptLink = db.StringProperty()

class Doctor( db.Model ):
    docName = db.StringProperty()
    docCode = db.StringProperty()

class Clinic( db.Model ):
    link   = db.StringProperty()
    date   = db.StringProperty()
    code   = db.StringProperty()
    doctor = db.ReferenceProperty( Doctor ) 
    dept   = db.ReferenceProperty( Department )

#class Clinic( db.Model ):
