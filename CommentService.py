from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch as urlfetch
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext.webapp.template import render
from google.appengine.api import users
import os
import uuid

from ShortLink import getShortUrl
from PasteService import Paste

class Comment(db.Model):
    user = db.UserProperty(required=True)
    time = db.DateTimeProperty(auto_now_add=True)
    paste = db.ReferenceProperty(Paste)
    comment = db.StringProperty()
    

class CommentService(webapp.RequestHandler):
    def post(self):
        loginType = self.request.get("userAuthType")
        if loginType not in ("google",):
            self.response.out.write(json.dumps({"result":"error","message":"Unsupported authentication type"}))
            return

        user = None
        if loginType == "google":
            user = users.get_current_user()
        if user is None:
            self.response.out.write(json.dumps({"result":"error","message":"Not logged in!"}))
            return

        comment = self.request.get("comment")
        if comment in (None,""):
            self.response.out.write(json.dumps({"result":"error","message":"Empty Code"}))
            return

        pasteid = self.request.get("pasteid")
        if pasteid in (None,""):
            self.response.out.write(json.dumps({"result":"error","message":"Empty Title"}))
            return
        
        p = None
        try:
            p = Paste.get_by_key_name(pasteid)
        except:
            pass
        if not p:
            self.response.out.write(json.dumps({"result":"error","message":"Invalid PasteId"}))
            return
        
        c = Comment(user=user, paste=p,comment=comment)
        c.put()
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.dumps({"result":"success"}))

    def get(self):
        pasteid = self.request.get("pasteid")
        if pasteid in (None,""):
            self.response.out.write(json.dumps({"result":"error","message":"Empty Title"}))
            return
        
        p = None
        try:
            p = Paste.get_by_key_name(pasteid)
        except:
            pass
        if not p:
            self.response.out.write(json.dumps({"result":"error","message":"Invalid PasteId"}))
            return
        self.response.out.write(json.dumps({"result":"success","data":getComments(p)}))

    @staticmethod
    def getComments(paste):
        c = Comment.all().filter("paste = ",paste).order("time")
        return map(lambda x:{"comment":x.comment,"time":str(x.time),"user":x.user.nickname()},c.fetch(c.count()))
