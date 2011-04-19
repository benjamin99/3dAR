# -*- coding: utf-8 -*-
import cgi
import datetime
import os
import urllib2
from BeautifulSoup import BeautifulSoup
from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Message

cwbUrl = 'http://www.cwb.gov.tw/V6/forecast/taiwan/36-p1-data.htm'

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
            context['browser']  = self.request.headers['User-Agent'] 
        
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
        
        # Get the id that indicate where is the start point of new messages:
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
            self.response.out.write('            <author>%s</author>\n' % msg.author.nickname() )
            self.response.out.write('            <postID>%d</postID>\n' % msg.postID )
            self.response.out.write('            <content>%s</content>\n' % msg.content )
            self.response.out.write('            <time>%s</time>\n' % msg.postDate )
            self.response.out.write('        </message>\n')            

        self.response.out.write('    </response>\n')

class FetchWeatherInfo(webapp.RequestHandler):
    def get(self):
        temperature = '11~23'
        rain_chance = '0%'
        city_name   = 'Test City'

        cityTag = self.request.get('city')
        if not cityTag:
            cityTag = 'TaipeiCityList'        
 
        # Fetch the information from CWB
        webpage = urllib2.urlopen(cwbUrl)
        soup = BeautifulSoup(webpage)
        # cityInfo = soup.find('tr', id='TaipeiCityList')
        
        if soup.find('tr', id= cityTag):
            city_name   = soup.find('tr', id= cityTag).contents[1].find('a').string
            temperature = soup.find('tr', id= cityTag).contents[3].find('a').string
            rain_chance = soup.find('tr', id= cityTag).contents[5].find('a').string

        # Dumping the xml content:
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.headers['Cache-Control'] = 'no-cache'
        self.response.out.write('<?xml version="1.0"?>\n')
        self.response.out.write('    <response>\n')
        self.response.out.write('        <cityname>%s</cityname>\n' % city_name )
        self.response.out.write('        <temperature>%s</temperature>\n' % temperature )
        self.response.out.write('        <rainchance>%s</rainchance>\n' % rain_chance )
        self.response.out.write('    </response>\n')


#--------------------------------------------------------------------

ROUTES = [
    ('/del', DeleteMyMessage),
    ('/fetch', FetchNewMessage),
    ('/logout', LogoutMe),
    ('/post', PostMyMessage),
    ('/weather', FetchWeatherInfo),
    ('/', MainPage),
]

application = webapp.WSGIApplication( ROUTES, debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
