# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=150)
    def __unicode__(self):
        return self.username
    class Meta:
        db_table = u'users'

class Trip(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    user = models.ForeignKey(User, db_column='FK_Users_ID') # Field name made lowercase.
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.
    comments = models.CharField(max_length=3072, db_column='Comments', blank=True) # Field name made lowercase.
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'trips'

class Icon(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.
    url = models.CharField(max_length=1536, db_column='URL') # Field name made lowercase.
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'icons'

class Position(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    user = models.ForeignKey(User, db_column='FK_Users_ID') # Field name made lowercase.
    trip = models.ForeignKey(Trip, null=True, db_column='FK_Trips_ID', blank=True) # Field name made lowercase.
    icon = models.ForeignKey(Icon, null=True, db_column='FK_Icons_ID', blank=True) # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude') # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude') # Field name made lowercase.
    altitude = models.FloatField(null=True, db_column='Altitude', blank=True) # Field name made lowercase.
    speed = models.FloatField(null=True, db_column='Speed', blank=True) # Field name made lowercase.
    angle = models.FloatField(null=True, db_column='Angle', blank=True) # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='DateAdded') # Field name made lowercase.
    dateoccurred = models.DateTimeField(null=True, db_column='DateOccurred', blank=True) # Field name made lowercase.
    comments = models.CharField(max_length=765, db_column='Comments', blank=True) # Field name made lowercase.
    imageurl = models.CharField(max_length=765, db_column='ImageURL', blank=True) # Field name made lowercase.
    signalstrength = models.IntegerField(null=True, db_column='SignalStrength', blank=True) # Field name made lowercase.
    signalstrengthmax = models.IntegerField(null=True, db_column='SignalStrengthMax', blank=True) # Field name made lowercase.
    signalstrengthmin = models.IntegerField(null=True, db_column='SignalStrengthMin', blank=True) # Field name made lowercase.
    batterystatus = models.IntegerField(null=True, db_column='BatteryStatus', blank=True) # Field name made lowercase.
    def __unicode__(self):
        return "{0}: ({1}, {2})".format(self.dateoccurred, self.latitude, self.longitude)
    class Meta:
        db_table = u'positions'
