from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from MainPage import MainPage
from PasteService import PasteService
from PasteShowService import PasteShowService
#import CommentService
from CommentService import CommentService
from PasteRedirectService import PasteRedirectService

l = []
l.append(('/',MainPage))
l.append(('/paste/',PasteService))
l.append(('/comment/',CommentService))
l.append(('/FromPasteId/',PasteRedirectService))


l.append(('/([-a-zA-Z0-9]+)',PasteShowService))

application = webapp.WSGIApplication(l,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
