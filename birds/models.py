from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime
from pytz import utc

class SpeciesFile(models.Model):
    species_list = models.FileField()

class Order(models.Model):
    order = models.CharField(max_length=100)

    def __str__(self):
        return self.order

class Family(models.Model):
    order = models.ForeignKey(Order)
    family_scientific = models.CharField(max_length=100)
    family_english = models.CharField(max_length=100)

    def __str__(self):
        return self.family_english+" "+self.family_scientific

class Genus(models.Model):
    family = models.ForeignKey(Family)
    genus = models.CharField(max_length=100)

    def __str__(self):
        return self.genus

class Species(models.Model):
    genus = models.ForeignKey(Genus, default=None)
    species = models.CharField(max_length=100, default=None)
    species_english = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return self.species+" "+self.species_english

class Subspecies(models.Model):
    species = models.ForeignKey(Species)
    subspecies = models.CharField(max_length=100)
    
    def __str__(self):
        return self.species.species_english+" "+self.species.genus.genus+" "+self.species.species+" "+self.subspecies

    def __unicode__(self):
        return self.species.species_english+" "+self.species.genus.genus+" "+self.species.species+" "+self.subspecies

class Sighting(models.Model):
    caption = models.CharField(max_length=100, default=None)
    post_text = models.CharField(max_length=1000, default=None, blank=True, null=True)
    #subspecies = models.ForeignKey(Subspecies, default=None, blank=True, null=True)
    species_tag = models.ForeignKey(Subspecies, default=None, blank=True, null=True)
    lat = models.FloatField(default=None)
    lng = models.FloatField(default= None)
    sighting_date = models.DateField()
    image = models.ImageField(default=None, blank=True, null=True)
    user_id = models.IntegerField(default=None)
    location = models.CharField(max_length=200, default=None, null=True, blank=True)
    post_ts = models.DateTimeField(auto_now_add=True)

    @property
    def time_diff(self):
        if self.post_ts:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.post_ts
            s = timediff.total_seconds()
            if s < 60:
                return "%0.0f seconds ago" % s
            elif s < 3600:
                return "%0.0f minutes ago" % ( s / 60.0 )
            else:
                return "%0.0f hours ago" % ( s / 3600.0 )
        
    @property
    def num_comments(self):
        return Comment.objects.filter( sighting = self.id ).count()
    
    @property
    def num_likes(self):
        return Like.objects.filter( sighting = self.id ).count()

    def __str__(self):
        return self.caption
    
class Like(models.Model):
    sighting = models.ForeignKey(Sighting)
    user = models.ForeignKey(User)
    
class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    sighting = models.ForeignKey(Sighting)
    viewed_by_user = models.BooleanField(default=False)
    post_ts = models.DateTimeField(auto_now_add=True)
    
class SpeciesVotes(models.Model):
    user = models.ForeignKey(User)
    species = models.ForeignKey(Subspecies)
    sighting = models.ForeignKey(Sighting)
    
