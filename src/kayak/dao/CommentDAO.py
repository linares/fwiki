'''
Created on Apr 17, 2011

@author: bigI
'''
import json

from ItemDAO import Item

class Comment(Item):

    def __init__(self, id=None):
        self.id = None
            
    def setFbArray(self, comment,  viewer_fbid):
        self.unique_id = comment['id']
        self.parent_id = comment['object_id']
        #self.viewer_fbid = comment['fromid']
        self.viewer_fbid = viewer_fbid
        self.type = 'comment'
        self.data = json.dumps(comment)


    def __repr__(self):
        return "<comment('%s','%d', '%s, %s')>" % (self.object_id, self.viewer_fbid, self.type, self.data)