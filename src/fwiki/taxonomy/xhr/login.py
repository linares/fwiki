'''
Created on Oct 2, 2011

@author: bigI
'''
# Create your views here.
import json
import urllib2
import string

from django.http import Http404
from fwiki.taxonomy.models import Node
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from django.core.exceptions import ObjectDoesNotExist


def distrib(request, endpoint):
    print request
    
    data = {"test" : "bla"}
    
    response = HttpResponse(json.dumps(data) , mimetype='application/json')
    
    response.set_cookie("test_pmt", "encrypted_auth_info") 
    
    return response



        