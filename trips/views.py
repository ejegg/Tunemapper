from django.http import HttpResponse
from django.template import Context, loader
from django.conf import settings
import json
import time
import datetime
import hashlib

from trips.models import Trip,User,Position

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
    if (request.is_ajax()):
        return HttpResponse(allString)
    
    template = loader.get_template('trips/index.html')
    allTrips = json.dumps(map(lambda t: {'name': t.name, 'id': t.id}, trips))

    context = Context({
        'selectedTrip' : selectedTrip,
        'allPos' : allString,
        'trips' : trips,
        'lastFmUrl' : settings.LAST_FM_URL,
        'mapsKey' : settings.GOOGLE_API_KEY
    })
    return HttpResponse(template.render(context))

def upload(request):
    username = request.REQUEST.get('u', '')
    pw = request.REQUEST.get('p', '')
    if (username == '' or pw == ''):
        return HttpResponse('Result:3')
    
    hashed = hashlib.md5('trackmeuser{0}'.format(pw)).hexdigest()
    user = None
    users = User.objects.filter(username=username, password=hashed)
    
    if (len(users) == 1):
        user = users[0]
    else:
        users = User.objects.filter(username=username)
        if (len(users) == 0):
            user = User(username=username, password=hashed)
            user.save();
        else:
            return HttpResponse(hashed)
    
    tripname = request.REQUEST.get('tn', '')
    action = request.REQUEST.get('a', '0')
    lat = request.REQUEST.get('lat', '0')
    lon = request.REQUEST.get('long', '0')
    dateoccurred = request.REQUEST.get('do', '1970-01-01 00:00:00')
    altitude = request.REQUEST.get('alt', '0')
    angle = request.REQUEST.get('ang', '0')
    speed = request.REQUEST.get('sp', '0')
    
    if (action == 'upload'):
        trip = None
        trips = Trip.objects.filter(name=tripname, user=user)
        if (len(trips) == 1):
            trip = trips[0]
        else:
            trip = Trip(name=tripname, user=user)
            trip.save()

        pos = Position(user = user, 
                       trip = trip,
                       latitude = float(lat),
                       longitude = float(lon),
                       altitude = float(altitude),
                       speed = float(speed),
                       angle = float(angle),
                       dateadded = datetime.datetime.now(),
                       dateoccurred = datetime.datetime.strptime(dateoccurred, '%Y-%m-%d %H:%M:%S', 'America/New_York'))
        pos.save()
        
        return HttpResponse('Result:0')