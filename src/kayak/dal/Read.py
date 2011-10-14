'''
Created on Apr 14, 2011

@author: bigI
'''

import memcache
import json

import boobox.config
import boobox.kayak.dal

#from boobox.kayak.dal import Session
import boobox.kayak.dal

from boobox.kayak.dao.ItemDAO import Item
from boobox.kayak.dao.PhotoDAO import Photo
from boobox.kayak.dao.UserDAO import User
#from Write import WriteDAL


class ReadDAL(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.__memcache = memcache.Client(boobox.config.MEMCACHE_SERVERS, debug=boobox.config.MEMCACHE_DEBUG_LEVEL)
        #self.__writeDAL = WriteDAL()
    
    def __getSession(self, obj):
        try:
            Session = boobox.kayak.dal.Session
            session = Session.object_session(obj)
            if session == None :
                session = Session()
        except:
            session.rollback()
        finally:
            session.close()
        return session
            
    def getItem(self, item):
        session = self.__getSession(item)
        return session.query(Item).filter_by(object_id=item.getObjectId()).first()    
    
    '''
        item:<item_id> => key
    '''
    def getFromUserIndex(self, key):
        try:
            item = self.__memcache.get(key)
            if item == None :
                session = boobox.kayak.dal.Session()
                item = session.query(Item).filter_by(object_id=key).first()
    #            self.__writeDAL.cacheItem(key, item.getData())
        except:
            session.rollback()
        finally:
            session.close()
            
        return item
    
    def getmulti(self, keys):
        return self.__memcache.get_multi(keys)
    
    
    '''
        user:<id> => key
    '''
    def getUser(self, fb_id):
        try:
            session = boobox.kayak.dal.Session()
            user = session.query(User).filter_by(fbid=fb_id).first()
        except:
            session.rollback()
            session.close()
        finally:
            session.close()
        return user
    
    def commitUser(self, user):
        try:
            session = self.__getSession(user)
            session.commit()
        except:
            session.rollback()
            
        finally:
            session.close()

    def getAlbumsPhotos(self, album):
        session = self.__getSession(album)
        return session.query(Photo).filter_by(unique_id=album.getObjectId()).first()

    '''
        search:<id> => key
    '''
    def getSearchID(self, search_id):
        return self.__memcache.get('search:' +  search_id)
    
    def searchFor(self, query):
        pass