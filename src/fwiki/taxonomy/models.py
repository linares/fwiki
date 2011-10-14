from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Node(models.Model):
    name = models.CharField(max_length=512)
    node_id = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=512)
    alias = models.TextField()
    contained_by = models.TextField()
    images = models.TextField()
    

class UserProfile(models.Model):
    
    #required for this model to be picked up as a recognized django user
    user = models.OneToOneField(User)
    
    fb_id = models.CharField(max_length=128)
    access_token = models.TextField()
    profile = models.TextField()
    

#def create_user_profile(sender, instance, created, **kwargs):
#    print "*********"
#    print vars(sender)
#    print instance
#    print created
#    print kwargs
#    print "*********"
#    
#    if created:
#        UserProfile.objects.create(user=instance, access_token="sdfasdf")
#
#
#post_save.connect(create_user_profile, sender=User)