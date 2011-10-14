'''
Created on Oct 10, 2011

@author: bigI
'''

import base64
import hashlib
import hmac
import simplejson as json
import urllib
import logging
import cgi

# create logger
_logger = logging.getLogger("FacebookUtils")
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


def base64_url_decode(inp):
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "="*padding_factor 
        return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))
    
def parse_signed_request(signed_request, secret):
    
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]
    
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))
    
    if data.get('algorithm').upper() != 'HMAC-SHA256':
        _logger.error('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()
    
    if sig != expected_sig:
        return None
    else:
        _logger.debug('valid signed request received..')
        return data
    
    
def get_fb_access_token(API_KEY, API_SECRET, REDIRECT_URI, code):
    args = dict(client_id=API_KEY,client_secret=API_SECRET,code=code,redirect_uri=REDIRECT_URI)
    
    _logger.debug("called get_fb_access_token()")
    _logger.debug("call = %s" , "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    
    response = cgi.parse_qs(urllib.urlopen(
                    "https://graph.facebook.com/oauth/access_token?" +
                    urllib.urlencode(args)).read())
    
    _logger.debug(response)
    
    return response["access_token"][-1]