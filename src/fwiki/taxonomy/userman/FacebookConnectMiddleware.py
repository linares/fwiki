'''
Created on Oct 2, 2011

@author: bigI
'''


# FacebookConnectMiddleware.py
from fwiki.taxonomy.utils.FacebookUtils import get_fb_access_token 

import md5
import time
import simplejson
import facebook
import sys
from datetime import datetime

import logging
from fwiki.taxonomy.utils import FacebookUtils
from fwiki.taxonomy.utils import UserUtils

# These values could be placed in Django's project settings
API_KEY = '139274172804886'
FWIKI_SESSION_COOKIE = 'fwiki_session'
FB_COOKIE_NAME = 'fbsr_'+API_KEY
API_SECRET = 'c8602e3ed04e27614601c75501e773ff'
REDIRECT_URI = 'http://localhost:8000/fb_login'
FB_LOGIN_PATH = '/fb_login'



PROBLEM_ERROR = 'There was a problem. Try again later.'
ACCOUNT_DISABLED_ERROR = 'Your account is not active.'
ACCOUNT_PROBLEM_ERROR = 'There is a problem with your account.'

class FacebookConnectMiddleware(object):
    
    reload(sys)
    sys.setdefaultencoding('iso-8859-1')
    
    # create logger
    _logger = logging.getLogger("FacebookConnectMiddleware")
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
    
    def process_request(self, request):
        try:
            #self._logger.debug(request.COOKIES)
            # Set the facebook message to empty. This message can be used to dispaly info from the middleware on a Web page.
            request.facebook_message = None
            # Don't bother trying FB Connect login if the user is already logged in
            if not request.user.is_authenticated() :            
                request.GET.items()
                if request.path == FB_LOGIN_PATH :
                    code = request.GET['code']
                    if not code == None :
                        #get the access token
                        access_token = get_fb_access_token(API_KEY, API_SECRET, REDIRECT_URI, code)
                        self._logger.debug(access_token)
                        
                        try:
                            graph = facebook.GraphAPI(access_token)
                            profile = graph.request("/me")
                            self._logger.debug(profile) 
                        except :
                            self._logger.debug(sys.exc_info())
                            request.error = sys.exc_info()
                        
                        #create a new account for this user
                        self._logger.debug('attempting to login a user')
                        UserUtils.loginUser(request, profile, access_token, API_SECRET)
                
                    
        # Something else happened. Make sure user doesn't have site access until problem is fixed.
        except:
            request.facebook_message = PROBLEM_ERROR
            self._logger.debug(sys.exc_info())
            
            #UserUtils.logoutUser(request)