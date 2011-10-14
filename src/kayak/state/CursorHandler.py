'''
Created on Apr 26, 2011

@author: bigI
'''

import json

import boobox.config

from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dal.Read import ReadDAL
from boobox.kayak.state.ResultNotifier import ResultNotifier

class CursorHandler(object):

    @staticmethod
    def orderByIndexTime(docs):
        sorted(docs, key=lambda doc:doc.get('indexed_at'))
        print docs
        return docs

    def __init__(self,**kwargs):
        self.__curr_cursor = kwargs.get('cursor')
        self.__searchId = kwargs.get('searchid')
        self.__cb = kwargs.get('callback')
        #self.__threshold = kwargs.get('threshold')
        self.__rdal = ReadDAL()
        self.__wdal = WriteDAL()
        
        self.__counter = 0
        self.__done = False
        
        self.__notificationBus = ResultNotifier()
        
    def addRawDocuments(self, docs):
        
        #CursorHandler.orderByIndexTime(docs)
        
        #Fetch from memcache
        c = []
        
        for doc in docs:
            item = json.loads(doc.get("full").encode('utf-8'))
            type = doc.get("type")
            
            c.append({"type" : type, "item" : item})
        
        
        #store the cached search
        self.__wdal.cacheSearchResult(self.__searchId, c)    
        if len(c) > self.__curr_cursor :
            #notify of result
            self.__notificationBus.notifyConditionWithResults(self.__searchId, c)
        
        
#    def addRawDocument(self, doc):
#        #Fetch from memcache
#        c = self.__rdal.getSearchID(self.__searchId)
#        
#        item = doc.get("full").encode('utf-8')
#        type = doc.get("type")
#        
#        #add to the cached result
#        if c == None:
#            c = [item]
#        else :
#            c.append({"type" : type, "item" : item})
#        
#        #store the cached search
#        self.__wdal.cacheSearchResult(self.__searchId, c)
#        
#        #if we're still looking to hit that threshold to return, then keep incrementing the counter
#        if not self.__done :
#            self.__counter += 1
#            if self.__counter >= self.__threshold :
#                self.__done = True
#                self.__cb(c)
                
            
        
    def isDone(self):
        return self.__done
    
    
    
    @staticmethod
    def getPageForSearchResults(result, cursor):
        page_size = boobox.config.PAGE_SIZE

        end = max([(cursor+1)*(page_size-1), len(result)])
        return result[cursor:end]