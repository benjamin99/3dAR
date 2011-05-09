# -*- coding: utf-8 -*-
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from main import apiPrefix


# -----------------------------------------------------------------
class TestFirstPost(webapp.RequestHandler):   # should return the page for testing
    def get(self):
        context = { 'postlink': '/'+apiPrefix+'/register',
                  }
        path =  os.path.join(os.path.dirname(__file__), 'templates',
                'firstPost.html')
        
        self.response.out.write(template.render(path, context))


class TestRePost(webapp.RequestHandler):
    def get(self):
        context = { 'postlink': '/'+apiPrefix+'/register',
                  }
        path =  os.path.join(os.path.dirname(__file__), 'templates',
                'rePost.html')
        
        self.response.out.write(template.render(path, context))

# -----------------------------------------------------------------
ROUTES = [
    ('/test/post', TestFirstPost),
    ('/test/repost', TestRePost),
]

application = webapp.WSGIApplication( ROUTES, debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

