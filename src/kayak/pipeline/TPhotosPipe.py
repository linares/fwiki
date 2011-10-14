'''
Created on Apr 10, 2011

@author: bigI
'''

import threading
import logging
import sys

from boobox.fetch.fb.fetchers.PhotosFetcher import PhotosFetcher
from boobox.fetch.fb.fetchers.Fetcher import Fetcher

from boobox.search.PhotosSearchAPI import PhotosSearchAPI
from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dao.PhotoDAO import Photo
from boobox.kayak.state.CapsuleManager import CapsuleManager

class TPhotosPipe(threading.Thread):

    NUM_ALBUMS_PER_QUERY = 40

    # create logger
    logger = logging.getLogger()
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

    '''
        doneCondition -- Meant to be used with a condition that's waiting on status
        index -- the Comments Index interface
        
    '''
    def __init__(self, doneCondition, albums, capsule):
        self.__doneCondition = doneCondition
        #self.__index_location = capsule.base() + capsule.user().getId()
        TPhotosPipe.logger.debug('INIT')
        self.__index = PhotosSearchAPI(capsule.user().getIndexLocation())
        self.__albums = albums
        self.__capsule = capsule
        self.__writeDAL = WriteDAL()
        super(TPhotosPipe, self).__init__()
        
    def run(self):
        self.__index.getEnv().attachCurrentThread()
        count = 0
        album_list= ''    
        
        for album in self.__albums :
            if count != 0 and count % TPhotosPipe.NUM_ALBUMS_PER_QUERY == 0:
                album_list = album_list[0:(len(album_list) - 1)]
                self.fetchPhotosForAlbums(album_list)
                count = 0
                album_list = ''
            else :
                album_list += album['aid']
                album_list += ','
                count += 1
            
        #finish up what's left
        if count != 0 :
            album_list = album_list[0:(len(album_list) - 1)]
            self.fetchPhotosForAlbums(album_list)
            count = 0
        
        self.__index.finish()
        
        self.__doneCondition.acquire()
        self.__doneCondition.notify()
        self.__doneCondition.release()
        
        TPhotosPipe.logger.debug('NOTIFIED DONE CONDITION')
        
        
    
    def fetchPhotosForAlbums(self, album_list):
       
        TPhotosPipe.logger.debug('getting photos in these albums : ' + album_list)
        c = PhotosFetcher(self.__capsule.user().getAccessToken(), album_list=album_list)
        
#        Fetcher.incrementalFetch(c, 100, self.fetchCallback)
        comments = c.fetchAll()
        self.fetchCallback(comments)
        
         
    def fetchCallback(self, photos):
        TPhotosPipe.logger.debug('indexing %(n)d' % {'n' : len(photos)})
        for photo in photos :
            try:
                p = Photo()
                p.setFbArray(photo, self.__capsule.user().getId())
                self.__writeDAL.persistItem(p)
                
            except Exception as e:
                TPhotosPipe.logger.error('WARNING, problem persisting the following photo')
                TPhotosPipe.logger.error(e)
                #TPhotosPipe.logger.warning(sys.exc_info()[0])
            
            try:
                self.__index.index(photo)
            except Exception as e:
                TPhotosPipe.logger.error('WARNING, problem indexing the following photo')
                TPhotosPipe.logger.error(e)
                #TPhotosPipe.logger.warning(sys.exc_info()[0])
                
            try:            
                capsules = CapsuleManager().capsulesForUser(self.__capsule.user().getId())
                for capsule in capsules:
                    capsule.updateState()
            except Exception as e :
                TPhotosPipe.logger.error('WARNING, problem following up in the State Capsule')
                TPhotosPipe.logger.error(e)
                #TPhotosPipe.logger.warning(sys.exc_info()[0])
