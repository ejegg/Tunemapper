from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper

import mimetypes
import json

from tracks.models import Track

def lookup(request, artist="", title=""):
    matchingTracks = Track.objects.filter(Q(id3artist__iexact = artist) | Q(id3v2artist__iexact = artist),
                                          Q(id3title__iexact = title) | Q(id3v2artist__iexact = title))
    if len(matchingTracks) == 0:
        matchingTracks = Track.objects.filter(Q(id3artist__icontains = artist) | Q(id3v2artist__icontains = artist),
                                          Q(id3title__icontains = title) | Q(id3v2artist__icontains = title))
    if len(matchingTracks) == 0:
        return HttpResponse("-1")
    
    return HttpResponse(matchingTracks[0].id)

def play(request, trackId):
    tracks = Track.objects.filter(pk=trackId)
    if len(tracks) == 0:
        return HttpResponse("")
    track = tracks[0]
    path = "/mp3s/{0}/{1}/{2}".format(track.album.artist.name, track.album.name, track.filename)
    wrapper = FileWrapper(open(path, "rb"))
    response = HttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = track.size
    response['Content-Disposition'] = "attachment; filename=" + track.filename
    return response
