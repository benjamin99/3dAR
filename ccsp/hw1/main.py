# -*- coding: utf-8 -*-
import cgi
import os
import datetime
from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Message

#--------------------------------------------------------------------
class MainPage(webapp.RequestHandler):
    def get(self):
        context = {}
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'postwall.html')
        
        user = users.get_current_user()
        if user:
            context['user'] = user.nickname()
            context['logout_link'] = users.create_logout_url('/')
        
        self.response.out.write(template.render(path, context))	
	
class LogoutMe(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('logout!')
 

class PostMyMessage(webapp.RequestHandler):
    def post(self):
        message = Message()
        
        user = users.get_current_user()
        if user:
            message.author = user

        #Added the content to the message: 
       	message.content = cgi.escape(self.request.get('content'))
        #Assigned the id to the message:
        message.postID = Message.max_id() + 1
	
        message.put()

class DeleteMyMessage(webapp.RequestHandler):
    def get(self):
        tar_id = int(self.request.get('id'))
        targets = Message.all().filter("postID =", tar_id)
        for msg in targets:
            msg.delete()

class FetchNewMessage(webapp.RequestHandler):
    def get(self):
        #Get the id that indicate where is the start point of new messages:
        current_id = int(self.request.get('id'))
        messages = Message.all().order('-postID').filter("postID > ", current_id)
        msg_set  = messages.fetch(10)
 
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.headers['Cache-Control'] = 'no-cache'
        
        # Start writing the xml content:
        self.response.out.write('<?xml version="1.0"?>\n')
        self.response.out.write('    <response>\n')
        self.response.out.write('        <id>%d</id>\n' % Message.max_id() )
        for msg in msg_set:
            self.response.out.write('        <message>\n')
            self.response.out.write('            <time>%s</time>\n' % msg.postDate )
            self.response.out.write('            <author>%s</author>\n' % msg.author.nickname() )
            self.response.out.write('            <postID>%d</postID>\n' % msg.postID )
            self.response.out.write('            <content>%s</content>\n' % msg.content )
            self.response.out.write('        </message>\n')            

        self.response.out.write('    </response>\n')

#--------------------------------------------------------------------

ROUTES = [
    ('/del', DeleteMyMessage),
    ('/fetch', FetchNewMessage),
    ('/logout', LogoutMe),
    ('/post', PostMyMessage),
    ('/', MainPage),
]

application = webapp.WSGIApplication( ROUTES, debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
