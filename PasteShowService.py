from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch as urlfetch
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext.webapp.template import render
from google.appengine.api import users
import os
from PasteService import Paste
from CommentService import CommentService

class PasteShowService(webapp.RequestHandler):
    def get(self,pasteId):
        user = users.get_current_user()
        if not user:
            user = {}
            user['nickname'] = 'Login'
            user['url'] = users.create_login_url(self.request.url)
        else:
            user.logoutURL = users.create_logout_url("/")
        
        #get the paste
        try:
            paste = Paste.get_by_key_name(pasteId)
            if not paste:
                raise Exception()
        except:
            self.response.out.write("Blah!")
            self.error(404)
            return
        #increment paste views
        try:
            if paste.user != user:
                paste.views += 1
                paste.put()
        except:
            pass
        
        comments = CommentService.getComments(paste)
        path = os.path.join(os.path.dirname(__file__), 'html/pasteShow.html')
        self.response.out.write(render(path, {'DATA':locals()}))
        
