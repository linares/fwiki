'''
Created on Apr 17, 2011

@author: bigI
'''

import json

from boobox.kayak.dao.ItemDAO import Item

from boobox.kayak.dal.Read import ReadDAL
from boobox.kayak.dal.Write import WriteDAL

class Album(Item):

    def __init__(self, id=None):
        self.id = id
        
    def setFbArray(self, album,  viewer_fbid):
        self.unique_id = album['aid']
        self.object_id = album['object_id']
        #self.viewer_fbid = album['owner']
        self.viewer_fbid = viewer_fbid
        self.parent_id = None
        self.type = 'album'
        self.data = json.dumps(album)

    def __repr__(self):
        return "<Album('%s','%d', '%s, %s')>" % (self.object_id, self.viewer_fbid, self.type, self.data)

    def getPhotos(self):
        # Need to fix this
        readDal = ReadDAL()
        
        #first query
        photos = readDal.getAlbumsPhotos(self)
        return photos
