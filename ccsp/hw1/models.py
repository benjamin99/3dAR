from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api.users import User


class Message(db.Model):
    content   = db.StringProperty()
    postDate  = db.DateTimeProperty(auto_now_add=True)
    user      = db.UserProperty()

