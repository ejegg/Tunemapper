from django.http import HttpResponse
from django.template import Context, loader
from django.conf import settings
import json
import time

from trips.models import Trip

def index(request, trackNum="0"):
    trackNum = int(trackNum)
    if (trackNum == 0 or trackNum > Trip.objects.count() -1):
        trackNum = Trip.objects.count() -1
    
    latest = Trip.objects.order_by('-id')[0:1].get()
    allPos = latest.position_set.all()    
    lastPos = latest.position_set.order_by('-dateoccurred')[0]
    template = loader.get_template('trips/index.html')
    def basics(pos):
        return {
            'time': long(time.mktime(pos.dateoccurred.timetuple())), 
            'lat': pos.latitude, 
            'long': pos.longitude,
            'spd': "{0} mph".format(pos.speed * 2.2369362920544)
        }
    allString = json.dumps(map(basics, allPos))
    context = Context({
        'latest' : latest,
        'lat' : "{0}".format(lastPos.latitude),
        'long' : "{0}".format(lastPos.longitude),
        'allPos' : allString,
        'lastFmUrl' : settings.LAST_FM_URL
    })
    return HttpResponse(template.render(context))