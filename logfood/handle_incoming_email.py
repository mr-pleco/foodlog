import logging, email
from google.appengine.api import users
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

from models import *
from util import *

class LogSenderHandler(InboundMailHandler):                
    def receive(self, mail_message):             
        body = get_clean_body(mail_message)
        
        #get user from mail_message.sender
        author = None
        
        if is_float_string(body):
            entry = WeightEntry()
            entry.weight = float(body)
            #check for duplicate date entries?
        else:                
            entry = FoodEntry()
            entry.content = body
        
        entry.author = author
        entry.put()


application = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)

def main():
   run_wsgi_app(application)
 
if __name__ == '__main__':
    main()