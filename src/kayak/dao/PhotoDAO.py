'''
Created on Apr 17, 2011

@author: bigI
'''
import json

from ItemDAO import Item

class Photo(Item):


    def __init__(self, id=None):
        self.id = id

    def setFbArray(self, photo, viewer_fbid):
        self.unique_id = photo['pid']
        self.object_id = photo['object_id']
        #self.viewer_fbid = photo['owner']
        self.viewer_fbid = viewer_fbid
        self.parent_id = photo['aid']
        self.type = 'photo'
        self.data = json.dumps(photo)

    def __repr__(self):
        return "<photo('%s','%d', '%s, %s')>" % (self.object_id, self.viewer_fbid, self.type, self.data)