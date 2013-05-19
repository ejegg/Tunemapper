from django.http import HttpResponse
from django.template import Context, loader
from django.conf import settings
import json
import time

from trips.models import Trip

def index(request, trackNum="0"):
    trackNum = int(trackNum)
    trips = Trip.objects.all();
    if (trackNum == 0):
        selectedTrip = Trip.objects.order_by('-id')[0:1].get()
    else:
        matchingTrips = filter(lambda t:t.id == trackNum, trips)
        if (len(matchingTrips) == 1):
            selectedTrip = matchingTrips[0]
        else: 
            return HttpResponse("Trip {0} not found".format(trackNum))
        
    allPos = selectedTrip.position_set.all()
    template = loader.get_template('trips/index.html')
    def basics(pos):
        if (pos.speed is None):
            pos.speed = 0;
        return {
            'time': long(time.mktime(pos.dateoccurred.timetuple())), 
            'lat': pos.latitude, 
            'long': pos.longitude,
            'spd': "{0} mph".format(pos.speed * 2.2369362920544)
        }
    allString = json.dumps(map(basics, allPos))
    allTrips = json.dumps(map(lambda t: {'name': t.name, 'id': t.id}, trips))
    context = Context({
        'selectedTrip' : selectedTrip,
        'allPos' : allString,
        'trips' : trips,
        'lastFmUrl' : settings.LAST_FM_URL,
        'mapsKey' : settings.GOOGLE_API_KEY
    })
    return HttpResponse(template.render(context))