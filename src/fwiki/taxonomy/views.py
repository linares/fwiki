# Create your views here.
import json
import urllib2
import string

from django.http import Http404
from fwiki.taxonomy.models import Node
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response

from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from django.core.exceptions import ObjectDoesNotExist

from fwiki.taxonomy.media import PhotoEnhance




def user_login(request):
    t = loader.get_template('fb_login.html')
    
    print request.COOKIES
    
    
    c = RequestContext(request, {
        'test' : 'test'
    })
    
    return HttpResponse(t.render(c))


def fb_login(request):
    return HttpResponseRedirect('/')

def index(request):
    
    t = loader.get_template('details.html')
    c = RequestContext(request, {
        'func': 'index'
    })

    return HttpResponse(t.render(c))    


def render_node(request, node_id):
    template_params = {}
    template_params['func'] = 'render_node'
    
    t = loader.get_template('node.html')
    debug = []
    
    node_id = '/' + node_id
    
    node = None
    
    #lookup the node_id
    try:
        node = Node.objects.get(node_id=node_id)
    except ObjectDoesNotExist :
        debug.append('Node ** %(node)s ** does NOT exist, pick something that we actually have' % { 'node' : node_id })
    except :
        debug.append('Totally crashed, bro')
        raise
     
     
    if node == None :
        template_params['debug'] = debug
        template_params['photos'] = []
        template_params['node'] = { 'name' : 'None, Sorry' }
    else :
        search_terms = []
        
        aliases = string.replace(string.replace(string.replace(node.alias, "u'", "'" ), "'", '"' ), '\\', '')
        aliases = json.loads(aliases)
        search_terms.extend(aliases)
        search_terms.append(node.name)
        
        #based on the metadata, go get outside info
        #photos = PhotoEnhance.grabFlickrPhotosFor(search_terms)
        
        debug.append('got Node with name : %(name)s' % {'name' : node.name})
        
        debug.append('got Node with images : %(images)s' % {'images' : node.images})
        
        template_params['debug'] = debug
        template_params['photos'] = json.loads(string.replace(string.replace(node.images, "u'", "'" ), "'", '"' ))
        template_params['node'] = node
        #based on the metadata, go get related social info
        
    c = RequestContext(request, template_params)

    return HttpResponse(t.render(c))    


def render_user(request, username):
    t = loader.get_template('details.html')
    c = RequestContext(request, {
        'func': 'render_user'
    })

    return HttpResponse(t.render(c))    



def render_usernode(request, username, node_id):
    t = loader.get_template('details.html')
    c = RequestContext(request, {
        'func': 'render_usernode'
    })

    return HttpResponse(t.render(c))    






def xhrDistrib(request):
    print request
    
    return HttpResponse({"bla" : "bla"}, mimetype='application/json')



        