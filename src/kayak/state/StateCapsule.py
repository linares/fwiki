'''
Created on Apr 5, 2011

@author: bigI
'''

import datetime
import md5

from mutex import mutex
from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dal.Read import ReadDAL
from boobox.kayak.dao.UserDAO import User
from boobox.search.QueryRetriever import QueryRetriever
from boobox.kayak.state.CapsuleManager import CapsuleManager

class StateCapsule(object):
    
    QUERY_THRESHOLD = 300
    
    '''
        query => string : query from the user
        partial => int : number of items for which the capsule returns on
        cb => function : callback when partial number is satisfied
        user_id => string : the FB ID of the user
        token => string : access token for the FB user
        index_loc => string : location of the user's index
    '''
    def __init__(self, **kwargs):
        self.__query = kwargs.get('query')
        self.__numItems = 0
        self.__mutex = mutex()
        #self.__fbid = kwargs.get('user_id')
        self.__user = kwargs.get('user')
        
        #self.__access_token = kwargs.get('token')
        #self.__index_location_base = kwargs.get('index_loc')

        self.__cursor_handler = kwargs.get('cursor_handler')
        self.__THRESHOLD_MULTIPLIER = 1

        # Not sure what this is doing?
        mda =  md5.new()
        mda.update(str(self.__user.getId()) + '-' + datetime.datetime.now().isoformat())
        self.__id = mda.hexdigest()  
        
    def _checkState(self, arg) :
        self.__numItems += 1
        
        if self.__numItems >= (StateCapsule.QUERY_THRESHOLD*self.__THRESHOLD_MULTIPLIER) :

            query_retriever = QueryRetriever(self.__user.getIndexLocation())

            ##WARNING!!! WE SHOULD PROBABLY DO THIS IN ANOTHER THREAD (this is a mutex'ed section!)
            #kick off a query to check for more results
            docs = query_retriever.search(self.__query)
            self.__cursor_handler.addRawDocuments(docs)
            self.__numItems = 0
            self.__THRESHOLD_MULTIPLIER +=1
            query_retriever.finish()

    def closeCapsule(self):
        CapsuleManager().removecapsule(self)
        #do whatever is needed here
 
    '''
    Thread safe setting an item
    '''
    def updateState(self):
        mutex.lock(self.__mutex, self._checkState, None)
        mutex.unlock(self.__mutex)
        
    '''
    Not thread safe, but a convenience method to grab the items in the queue
    '''
    def items(self):
        return self.__items


    def user(self):
        return self.__user

#    def token(self):
#        return self.__access_token
#
#    def fbid(self):
#        return self.__fbid
#
#    def base(self):
#        return self.__index_location_base
#
#    def index_location(self):
#        return self.__index_location_base + self.__fbid
#
    def cursor_handler(self):
        return self.__cursor_handler
    
    def query(self):
        return self.__query
    
    '''
        Called when we're finished fetching/indexing for this user.
        We just need to make sure we turn the 'indexing' field to OFF (to kick off subsequent indexing/fetching)
    '''
    def updateUser(self):
        rdal = ReadDAL()
        #user = rdal.getUser(self.__fbid)
        self.__user.setIndexing(0)
        rdal.commitUser(self.__user)
    
    
    def capsuleID(self):
        return self.__id


    @staticmethod
    def createSearchID(fbid, query):
        mda =  md5.new()
        mda.update(fbid + ':' + query)
        search_id = mda.hexdigest()
        return search_id
    
    
def test(items) : 
    print 'done'
    print items

if __name__ == "__main__":
    s = StateCapsule(3, test) 
    for i in range(7) :
        s.setItem(i)
        