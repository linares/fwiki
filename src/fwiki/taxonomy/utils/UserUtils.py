'''
Created on Oct 11, 2011

@author: bigI
'''
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from fwiki.taxonomy.models import UserProfile
from fwiki.taxonomy.utils.FacebookUtils import parse_signed_request,get_fb_access_token 

import md5
import time
import json
import facebook
import sys
import logging

from datetime import datetime


PROBLEM_ERROR = 'There was a problem. Try again later.'
ACCOUNT_DISABLED_ERROR = 'Your account is not active.'
ACCOUNT_PROBLEM_ERROR = 'There is a problem with your account.'

# create logger
_logger = logging.getLogger("UserUtils")
_logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
_logger.addHandler(ch)


def loginUser(request, profile, access_token, API_SECRET):
    
    user_id = profile['id']
    
    try:
        # Try to get Django account corresponding to friend
        # Authenticate then login (or display disabled error message)
        django_user = User.objects.get(username=user_id)
        user = authenticate(username=user_id, 
                            password=md5.new(user_id + settings.SECRET_KEY).hexdigest())
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                request.facebook_message = ACCOUNT_DISABLED_ERROR
        else:
            request.facebook_message = ACCOUNT_PROBLEM_ERROR
           
    except User.DoesNotExist:
        _logger.debug('user doesnt exist, creating')
        createUser(request, profile, access_token)
        user = authenticate(username=user_id, 
                            password=md5.new(user_id + settings.SECRET_KEY).hexdigest())
        login(user)

def logoutUser(request, profile):
    pass

def createUser(request, profile, access_token):
    user_id = profile['id']
    first_name = profile['first_name']
    last_name = profile['last_name']
    
    # Create user
    user = User.objects.create(username=user_id, email=profile['email'],password=md5.new(user_id + settings.SECRET_KEY).hexdigest(), first_name=first_name, last_name=last_name)

    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        #create profile - CUSTOMIZE THIS LINE TO OYUR MODEL:
        profile = UserProfile(user_id=user.id, fb_id=user_id, access_token=access_token,profile=json.dumps(profile))
        profile.save()

#    profile.access_token = access_token
#    profile.user_id = user_id
#    profile.profile = json.dumps(profile)
#    profile.save()
    
    return user
    
    