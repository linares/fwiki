'''
Created on Aug 20, 2011

@author: bigI
'''

import flickrapi
import json

FLICKR_API_KEY = '4c7e21d715fb8d7c6f776aa72d9cd016'
FLICKR_API_SECRET = '78d996d9a0854424'


def grabFlickrPhotosFor(names, mobile=False):
    flickr = flickrapi.FlickrAPI(FLICKR_API_KEY)
    
    photo_urls=[]
    
    for name in names :
        print name 
        photos_json = flickr.photos_search(text=name, per_page=5, format='json')
        cut_index = photos_json.find('(')
        photos_json = photos_json[cut_index + 1:(len(photos_json) - 1)]
        photos = json.loads(photos_json)
        if not photos == None:
            photos = photos.get('photos')
            if not photos == None :
                photos = photos.get('photo')
                for item in photos : 
                    photoURL = 'http://farm' + str(item.get('farm')) + '.static.flickr.com/' + item.get('server') + '/' + item.get('id') + '_' + item.get('secret')
                    if mobile :
                        photoURL +=  '_m.jpg'
                    else :
                        photoURL += '.jpg'
                    
                    photo_urls.append(photoURL)

    
    return photo_urls
    
if __name__ == '__main__':
    grabFlickrPhotosFor([u'la ville des lumi\\xe8res', u'paris, france', u'city of light', u'paris-france'])