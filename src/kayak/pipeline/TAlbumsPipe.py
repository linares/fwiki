'''
Created on Apr 17, 2011

@author: bigI
'''

import threading
import logging
import sys

from boobox.fetch.fb.fetchers.Fetcher import Fetcher 

from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dao.AlbumDAO import Album
from boobox.kayak.state.CapsuleManager import CapsuleManager

import boobox.context.tag.tagger

'''
    Thread class that takes care of generic incremental fetching encapsulation
'''    
class TAlbumsPipe(threading.Thread):
    
    NUM_ALBUMS_PER_QUERY = 40

    # create logger
    logger = logging.getLogger("TAlbumsPipeLogger")
    #logger.setLevel(logging.DEBUG)
    
    # create console handler and set level to debug
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)
    
    # create formatter
    #formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s")
    
    # add formatter to ch
    #ch.setFormatter(formatter)
    
    # add ch to logger
    #logger.addHandler(ch)
    
    def __init__(self, fetcher, index , capsule, doneCondition, incrementalCallback=None, incrementalArguments=None):
        self.__capsule = capsule
        self.__fetcher = fetcher
        self.__incrementalCallback = incrementalCallback
        self.__incrementalArguments = incrementalArguments
        self.__index = index
        self.__doneCondition = doneCondition
        self.__stillIndexingCondition = threading.Condition()
        self.__writeDAL = WriteDAL()
        super(TAlbumsPipe, self).__init__()
        
    def _aggregate(self, items):
        TAlbumsPipe.logger.debug('indexing %(n)d' % {'n' : len(items)})
        try:
            for item in items :
                
                try:
                    album = Album()
                    album.setFbArray(item, self.__capsule.user().getId())
                    
                    self.__writeDAL.persistItem(album)
                    
                    
                except Exception as e :
                    TAlbumsPipe.logger.error('WARNING, problem persisting album')
                    TAlbumsPipe.logger.error(e)
                    #TAlbumsPipe.logger.warning(sys.exc_info()[0])
                    
                try:
                    self.__index.index(item)
                except Exception as e :
                    TAlbumsPipe.logger.error('WARNING, problem indexing album')
                    TAlbumsPipe.logger.error(e)
                    #TAlbumsPipe.logger.warning(sys.exc_info()[0])
                
                try:
                    capsules = CapsuleManager().capsulesForUser(self.__capsule.user().getId())
                    for capsule in capsules:
                        capsule.updateState()
                except Exception as e :
                    TAlbumsPipe.logger.error('WARNING, problem following up in the State Capsule')
                    #TAlbumsPipe.logger.warning(sys.exc_info()[0])
                    TAlbumsPipe.logger.error(e)
        except:
            TAlbumsPipe.logger.error('WARNING, problem indexing the following album')
            TAlbumsPipe.logger.warning(sys.exc_info()[0])
            
            
       
        
        
        if self.__incrementalCallback != None :
            self.__incrementalCallback(items, self.__incrementalArguments)

    def run(self):
        self.__index.getEnv().attachCurrentThread()
        Fetcher.incrementalFetch(self.__fetcher, 10, self._aggregate)
        
        #only do this when we're sure we've indexed and captured everything
        self.__doneCondition.acquire()
        self.__doneCondition.notify()
        self.__doneCondition.release()
        #this signifies the thread is done running