from google.appengine.ext import db

class Account(db.Model):
    user = db.UserProperty() #fixme key on user_id for longterm stability
    mail_address = db.StringProperty()    

class FoodEntry(db.Model):
    content = db.StringProperty()
    
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class WeightEntry(db.Model):
    weight = db.FloatProperty()
    
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class PicEntry(db.Model):
    picture = db.BlobProperty(default=None)
    weight = db.FloatProperty()
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)