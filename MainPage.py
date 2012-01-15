from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch as urlfetch
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext.webapp.template import render
from google.appengine.api import users
import os

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            user = {}
            user['nickname'] = 'Login'
            user['url'] = users.create_login_url("/")
        else:
            user.logoutURL = users.create_logout_url("/")
        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(render(path, {'DATA':locals()}))
