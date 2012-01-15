from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch as urlfetch
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext.webapp.template import render
from google.appengine.api import users
import os
import uuid
from PasteService import Paste

class PasteRedirectService(webapp.RequestHandler):
    def get(self):
        pid = self.request.get("id")
        
        r = Paste.all().filter("pasteId =",pid)
        if not r.count():
            self.error(404)
            return
        p = r.fetch(1)[0]
        self.redirect("/" + str(p.key().name()))
