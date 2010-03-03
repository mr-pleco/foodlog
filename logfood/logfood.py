import os
from datetime import datetime, timedelta

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import pygooglechart as gchart
from google.appengine.api import images

from models import *
from util import *


class Index(webapp.RequestHandler):
    def get_weight_data(self, width_days):        
        time_window = timedelta(width_days)
        now = datetime.now()
        start_time = now - time_window
        #print time_window, now, start_time
        
        weights = WeightEntry.all()
        weights.filter('date >=', start_time)
        
        ww = [w.weight for w in weights]
        dd = [days_between(w.date, start_time) for w in weights]

        #test data
        #dd = [x + .3 for x in range(7)]
        #ww = [195,197,200,200,204,206,207]

        return dd,ww

    def make_weight_chart_url(self, weight_data, width_days=7):
        days, weights = weight_data
        if days == []:
            return '' #empty image url

        min_y = nearest_5(min(weights)*.95)
        max_y = nearest_5(max(weights)*1.02)
        dy = max_y - min_y
        
        x_range = [0, width_days] #last week of data        
        y_range = [min_y, max_y]
        
        chart = gchart.XYLineChart(630, 200, y_range=y_range, x_range=x_range)
        chart.add_data(days)
        chart.add_data(weights)
        
        chart.set_colours(['0000FF']) # Set the line colour to blue
        #chart.fill_linear_stripes(gchart.Chart.CHART, 0, 'CCCCCC', 0.25, 'FFFFFF', 0.25)\
        
        y_spacing = 5 #units
        chart.set_grid(0, 100./dy*y_spacing, 5, 5) #vert, horiz, line, spacing (px)
 
        y_labels = range(min_y, max_y+y_spacing, y_spacing)
        chart.set_axis_labels(gchart.Axis.LEFT, y_labels)
        
        now = datetime.now()
        x_labels = [(now - timedelta(t)).strftime(r'%m/%d') for t in range(width_days+1,0,-1)]
        chart.set_axis_labels(gchart.Axis.BOTTOM, x_labels)
        
        return chart.get_url()
    
    def get(self):
        try:
            width_days = int(self.request.get("d")) or 7
        except ValueError:
            width_days = 7
        weight_data = self.get_weight_data(width_days)

        params = {}
        params['dates'] = weight_data[0]
        params['weights'] = weight_data[1]
        params['weight_img_url'] = self.make_weight_chart_url(weight_data,width_days)
        params.update(make_logon_anchor_params(self))

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, params))

class GetPic(webapp.RequestHandler):
    def get(self):
        when_str = self.request.get('when')
        picentry = getPic(when_str)
        if (picentry and picentry.picture):
            picdata = picentry.picture
            picdata = images.resize(picdata, width=300)
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(picdata)
        else:
            self.redirect('/static/noimage.jpg')
    
def getPic(when_str):
    if when_str=='last':
        result = db.GqlQuery("SELECT * FROM PicEntry order by date desc LIMIT 1").fetch(1)
        if (len(result) > 0):
            return result[0]
        return
    elif when_str=='heaviest':
        result = db.GqlQuery("SELECT * FROM PicEntry order by weight LIMIT 1").fetch(1)
        if (len(result) > 0):
            return result[0]
        return

application = webapp.WSGIApplication(
    [('/', Index),
     ('/pic', GetPic)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()