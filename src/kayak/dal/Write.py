'''
Created on Apr 14, 2011

@author: bigI
'''

import memcache
import boobox

import boobox.config
import boobox.kayak.dal
import boobox.kayak.dao

#from boobox.kayak.dal import Session


class WriteDAL(object):
    '''
        Abstracts the persisting part to the backend
    '''
    
    '''
    PERSIST
    '''
    
    COUNT_BEFORE_COMMIT = 10
    
    def __init__(self):
        self.__memcache = memcache.Client(boobox.config.MEMCACHE_SERVERS, debug=boobox.config.MEMCACHE_DEBUG_LEVEL)
        self.count = 0
    
    def __getSession(self, obj):
        Session = boobox.kayak.dal.Session
        session = Session.object_session(obj)
        if session == None :
            session = boobox.kayak.dal.Session()
        return session
    
    def persistItem(self, item):
        session = self.__getSession(item)
        return self.__persistItem(item, session)
           
    def __persistItem(self , item, session):
        try:
            self.count += 1
            session.add(item)
            if self.count >= WriteDAL.COUNT_BEFORE_COMMIT :
                session.commit()
                session.close()
        except:
            session.rollback()
            session.close()
    
    def persistItems(self, items):
        for item in items :
            session = self.__getSession(item)
            self.__persistItem(item, session)
    
    def deleteItem(self, item):
        try:
            session = self.__getSession(item)
            session.delete(item)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()
    
    def persistUser(self, user):
        try:
            session = self.__getSession(user)
            session.add(user)
            session.commit()
        except:
            session.rollback()
            session.close()
        
    def updateUser(self, user):
        try:
            session = self.__getSession(user)
            session.save(user)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()
    
    def deleteUser(self, user):
        try:
            session = self.__getSession(user)
            session.delete(user)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()

    def deleteAllItemsUser(self,fbid):
        try:
            Item = boobox.kayak.dao.ItemDAO.Item
            session = boobox.kayak.dal.Session()
            session.query(Item).filter(Item.viewer_fbid==fbid).delete()
            session.commit()
        except:
            session.rollback()
            session.close()

    '''
    CACHING
    '''
    
    def cacheItem(self, key, val):
        return self.__memcache.set(key, val,20)
        
    '''
        Expecting the kvpairs to be a map of { "k" : "v", ...}
    '''
    def cacheItems(self, kvpairs):
        return self.__memcache.set_multi(kvpairs)
    
    
    
    def cacheSearchResult(self, search_id , result):
        return self.cacheItem('search:' +  search_id, result)
    
    