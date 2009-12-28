from google.appengine.api import users

def make_logon_anchor_params(webapp_instance):
    if users.get_current_user():
        logon_url = users.create_logout_url(webapp_instance.request.uri)
        logon_url_text = 'Logout'
    else:
        logon_url = users.create_login_url(webapp_instance.request.uri)
        logon_url_text = 'Login'
    
    params = {'logon_url':logon_url,
              'logon_url_text':logon_url_text}
    return params


def nearest_5(num):
    return round(num*2,-1)/2.
    
def days_between(last, first):
    dur = last - first
    days = dur.days + dur.seconds / 86400.
    return days

def get_clean_body(mail_message):
    bodies = mail_message.bodies(content_type='text/plain') #generator
    
    allBodies = ""; numBodies=0
    for body in bodies:
        allBodies = allBodies + body[1].decode()
        numBodies += 1
        if isinstance(allBodies, unicode):
            allBodies = allBodies.encode('utf-8')
    
    
    if numBodies > 1: logging.warn("recvd mail with %s bodies: %s" % (numBodies, mail_message))
    return allBodies

def is_float_string(str):
    try:
        dummy = float(str)
        return True
    except ValueError:
        return False