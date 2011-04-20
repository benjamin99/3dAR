from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api.users import User


class Message(db.Model):
    content   = db.StringProperty()
    postDate  = db.DateTimeProperty(auto_now_add=True)
    postID    = db.IntegerProperty()
    author    = db.UserProperty()
    rCount    = db.IntegerProperty(default=1)
    isRemoved = db.BooleanProperty(default=False)    
 
    def retain(self):
        count = self.rCount;
        self.rCount = count + 1
        self.put();
    
    def release(self):
        self.isRemoved = True;
        self.rCount = self.rCount - 1;
        self.put();    

    def check2Delete(self):
        if self.rCount < 1:
            self.delete();   
 
    def max_id():
        messages = Message.all().order('-postID')
        max_id_msg = messages.get() 
        if max_id_msg:
            return max_id_msg.postID
        else:
            return 0
    
    max_id = staticmethod(max_id)
