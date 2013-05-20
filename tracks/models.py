# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

#class Albumart(models.Model):
#    id = models.IntegerField(null=True, primary_key=True, blank=True)
#    album = models.IntegerField(null=True, blank=True)
#    name = models.TextField(blank=True)
#    size = models.IntegerField(null=True, blank=True)
#    class Meta:
#        db_table = u'albumart'

class Artist(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    name = models.TextField(unique=True, blank=True)
    class Meta:
        db_table = u'artists'
        app_label = 'tracks'

class Album(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    artist = models.ForeignKey(Artist, db_column=u'artist')
    name = models.TextField(blank=True)
    class Meta:
        db_table = u'albums'
        app_label = 'tracks'
        
#class Subalbums(models.Model):
#    id = models.IntegerField(null=True, primary_key=True, blank=True)
#    album = models.IntegerField(null=True, blank=True)
#    name = models.TextField(blank=True)
#    sortorder = models.IntegerField(null=True, db_column=u'sortOrder', blank=True) # Field name made lowercase.
#    class Meta:
#        db_table = u'subAlbums'

class Track(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=True)
    album = models.ForeignKey(Album, db_column=u'album')
    size = models.IntegerField(null=True, blank=True)
    subalbum = models.IntegerField(null=True, db_column=u'subAlbum', blank=True) # Field name made lowercase.
    filename = models.TextField(db_column=u'fileName', blank=True) # Field name made lowercase.
    sortorder = models.IntegerField(null=True, db_column=u'sortOrder', blank=True) # Field name made lowercase.
    id3title = models.TextField(db_column=u'id3Title', blank=True) # Field name made lowercase.
    id3album = models.TextField(db_column=u'id3Album', blank=True) # Field name made lowercase.
    id3artist = models.TextField(db_column=u'id3Artist', blank=True) # Field name made lowercase.
    id3year = models.TextField(db_column=u'id3Year', blank=True) # Field name made lowercase.
    id3comment = models.TextField(db_column=u'id3Comment', blank=True) # Field name made lowercase.
    id3track = models.IntegerField(null=True, db_column=u'id3Track', blank=True) # Field name made lowercase.
    id3genre = models.IntegerField(null=True, db_column=u'id3Genre', blank=True) # Field name made lowercase.
    id3v2title = models.TextField(db_column=u'id3v2Title', blank=True) # Field name made lowercase.
    id3v2album = models.TextField(db_column=u'id3v2Album', blank=True) # Field name made lowercase.
    id3v2artist = models.TextField(db_column=u'id3v2Artist', blank=True) # Field name made lowercase.
    id3v2albumsort = models.TextField(db_column=u'id3v2AlbumSort', blank=True) # Field name made lowercase.
    id3v2artistsort = models.TextField(db_column=u'id3v2ArtistSort', blank=True) # Field name made lowercase.
    id3v2albumartist = models.TextField(db_column=u'id3v2AlbumArtist', blank=True) # Field name made lowercase.
    id3v2year = models.TextField(db_column=u'id3v2Year', blank=True) # Field name made lowercase.
    id3v2track = models.TextField(db_column=u'id3v2Track', blank=True) # Field name made lowercase.
    id3v2disc = models.TextField(db_column=u'id3v2Disc', blank=True) # Field name made lowercase.
    id3v2totaltracks = models.TextField(db_column=u'id3v2TotalTracks', blank=True) # Field name made lowercase.
    id3v2totaldiscs = models.TextField(db_column=u'id3v2TotalDiscs', blank=True) # Field name made lowercase.
    id3v2genre = models.TextField(db_column=u'id3v2Genre', blank=True) # Field name made lowercase.
    bitrate = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    catalogtime = models.DateTimeField(null=True, db_column=u'catalogTime', blank=True) # Field name made lowercase.
    error = models.TextField(blank=True)
    class Meta:
        db_table = u'tracks'
        app_label = 'tracks'

