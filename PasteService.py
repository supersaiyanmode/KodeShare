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

class Paste(db.Model):
    user = db.UserProperty(required=True)
    time = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    code = db.BlobProperty(required=True)
    language = db.StringProperty()
    views = db.IntegerProperty(default=0)
    commentsEnabled = db.BooleanProperty()
    #used for redirection stuff
    pasteId = db.StringProperty()

class PasteService(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url("/paste/"))
            return
        else:
            user.logoutURL = users.create_logout_url("/")
        #fetch all previous pastes
        p = Paste.all().filter("user =",user).order("-time")
        pastes = p.fetch(p.count())
        
        path = os.path.join(os.path.dirname(__file__), 'html/userPastes.html')
        self.response.out.write(render(path, {'DATA':locals()}))

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

        language = self.request.get("language")
        if language not in ("C","C++","Java"):
            self.response.out.write(json.dumps({"result":"error","message":"Language not supported"}))
            return

        code = self.request.get("code")
        if code in (None,""):
            self.response.out.write(json.dumps({"result":"error","message":"Empty Code"}))
            return

        title = self.request.get("title")
        if code in (None,""):
            self.response.out.write(json.dumps({"result":"error","message":"Empty Title"}))
            return
        
        commentsEnabled = False
        if self.request.get("commentsEnabled"):
            commentsEnabled = True
        
        #generate pasteId
        c = str(uuid.uuid4())
        while Paste.all().filter("pasteId =",c).count():        #assume the while loop terminates sometime! :P
            c = str(uuid.uuid4())
            
        key = None
        try:
            url = getShortUrl("http://kode-share.appspot.com/FromPasteId/?id="+c)
            key = url[len('http://goo.gl/'):]
        except:
            key = str(uuid.uuid4())
        p = Paste(key_name=key,user=user,code=str(code),language=language, title=title,
                    commentsEnabled = commentsEnabled,pasteId=c)
        p.put()
        
        self.redirect("/"+key)
        
        
