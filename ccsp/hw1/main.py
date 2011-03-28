# -*- coding: utf-8 -*-
import os
import datetime
from google.appengine.api import users 
from google.appengine.ext import webapp
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
 

class AddMyMessage(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Add ....')


class DeleteMyMessage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Delete ... ')

#--------------------------------------------------------------------

ROUTES = [
    ('/add', AddMyMessage),
    ('/del', DeleteMyMessage),
    ('/logout', LogoutMe),
    ('/', MainPage),
]

application = webapp.WSGIApplication( ROUTES, debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
