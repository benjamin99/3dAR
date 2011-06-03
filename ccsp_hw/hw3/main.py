# -*- coding: utf-8 -*-
import os
import re
import urllib
import urllib2
import datetime
import facebook
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

FACEBOOK_APP_ID = "119095881507748"
FACEBOOK_APP_SECRET = "8268563eb67cbf05183086ac835b4d47"

# facebook ----------------------------------------
class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)


class BaseHandler(webapp.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user




# -------------------------------------------------
class MainHandler(BaseHandler):
    def get(self):
        user = self.current_user
        path = os.path.join(
			os.path.dirname(__file__), 'templates', 
			'mainJqt.html' )

	self.response.out.write( template.render(path,{  'user':user }) )

class FbLoginHelper(BaseHandler):
    def get(self):
        self.response.out.write('fblogin!')

# -------------------------------------------------

ROUTES = [
    ('/fblogin', FbLoginHelper),
    ('/', MainHandler),
]

application = webapp.WSGIApplication( ROUTES, debug = True )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
