'''
Created on Apr 24, 2011

@author: bigI
'''
import boobox.config
from boobox.search.SearchAPI import SearchAPI

class User(object):

    __tablename__ = 'booboxapp_userindex'

    '''
        Assumes a user map
    '''
    def __init__(self, fbid):
        self.fbid = fbid
        #self.fbid = user['fbid']
        #self.access_token = user['access_token']
        #self.fbsession = user['fbsession']
        #self.index_time = user['index_time']
        #self.created = user['created']
        #self.indexing = user['indexing']
     
    def getId(self):
        return self.fbid
    
    def getIndexing(self):
        return self.indexing
    
    def getIndexTime(self):
        return self.index_time
    
    def getFbSession(self):
        return self.fbsession 

    def getAccessToken(self):
        return self.access_token

    def getCreated(self):
        return self.created

    def setAccessToken(self, val):
        self.access_token = val
    
    def setIndexing(self, val):
        self.indexing = val

    def setIndexTime(self, val):
        self.index_time = val

    def setCreated(self, val):
        self.created = val

    def getIndexLocation(self):
        """Returns the index location for the user"""
        index_location = boobox.config.INDEX_LOCATION + str(self.fbid) + "/"
        return index_location

    def prepFirstUse(self):
        #Create user index
        SearchAPI.createIndex(self.getIndexLocation())

    def __repr__(self):
        return "<user('%d','%s', '%s', '%s', '%d')>" % (self.fbid, self.fbsession, self.index_time, self.created, self.indexing)
        