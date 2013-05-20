from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
import json

from tracks.models import Track

def lookup(request, artist="", title=""):
    matchingTracks = Track.objects.filter(Q(id3artist__icontains = artist) | Q(id3v2artist__icontains = artist),
                                          Q(id3title__icontains = title) | Q(id3v2artist__icontains = title))
    if len(matchingTracks) == 0:
        return HttpResponse("[]")
    
    track = matchingTracks[0]
    path = "file:///mp3s/{0}/{1}/{2}".format(track.album.artist.name, track.album.name, track.filename)
    
    return HttpResponse(json.dumps(path))