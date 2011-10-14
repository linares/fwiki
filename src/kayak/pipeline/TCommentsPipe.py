'''
Created on Apr 10, 2011

@author: bigI
'''

import threading
import logging
import sys

from boobox.fetch.fb.fetchers.CommentsFetcher import CommentsFetcher
from boobox.fetch.fb.fetchers.Fetcher import Fetcher

from boobox.search.CommentsSearchAPI import CommentsSearchAPI
from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dao.CommentDAO import Comment
from boobox.kayak.state.CapsuleManager import CapsuleManager

class TCommentsPipe(threading.Thread):

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
        TCommentsPipe.logger.debug('INIT')
        self.__index = CommentsSearchAPI(capsule.user().getIndexLocation())
        self.__albums = albums
        self.__capsule = capsule
        self.__writeDAL = WriteDAL()
        super(TCommentsPipe, self).__init__()
        
    def run(self):
        self.__index.getEnv().attachCurrentThread()
        count = 0
        album_list= ''    
        
        for album in self.__albums :
            if count != 0 and count % TCommentsPipe.NUM_ALBUMS_PER_QUERY == 0:
                album_list = album_list[0:(len(album_list) - 1)]
                self.fetchCommentsForAlbums(album_list)
                count = 0
                album_list = ''
            else :
                album_list += album['aid']
                album_list += ','
                count += 1
            
        #finish up what's left
        if count != 0 :
            album_list = album_list[0:(len(album_list) - 1)]
            self.fetchCommentsForAlbums(album_list)
            count = 0
        
        self.__index.finish()
        
        self.__doneCondition.acquire()
        self.__doneCondition.notify()
        self.__doneCondition.release()
        
        TCommentsPipe.logger.debug('NOTIFIED DONE CONDITION')
        
        
    
    def fetchCommentsForAlbums(self, album_list):
       
        TCommentsPipe.logger.debug('getting comments for photos in these albums : ' + album_list)
        c = CommentsFetcher(self.__capsule.user().getAccessToken(), object_ids='SELECT object_id FROM photo WHERE aid IN (%(list)s)' % {'list' : album_list })
        
#        Fetcher.incrementalFetch(c, 100, self.fetchCallback)
        num_retries = 0
        comments = []
        while num_retries < 3 :
            
            try:
                comments = c.fetchAll()
            except Exception as e:
                num_retries += 1
                self.logger.warning(e)
                continue
            
            break
        
        self.fetchCallback(comments)
        
         
    def fetchCallback(self, comments):
        TCommentsPipe.logger.debug('indexing %(n)d' % {'n' : len(comments)})
        for comment in comments :
            try:
                
                c = Comment()
                c.setFbArray(comment,  self.__capsule.user().getId())
                self.__writeDAL.persistItem(c)
                self.__index.index(comment)
                

            except Exception as e:
                TCommentsPipe.logger.error('WARNING, problem persisting the following comment')
                TCommentsPipe.logger.error(e)
                #TCommentsPipe.logger.warning(sys.exc_info()[0])
         
            try:
                self.__index.index(comment)
            except Exception as e:
                TCommentsPipe.logger.error('WARNING, problem indexing the following comment')
                TCommentsPipe.logger.error(e)
                #TCommentsPipe.logger.warning(sys.exc_info()[0])
            
            try:
                capsules = CapsuleManager().capsulesForUser(self.__capsule.user().getId())
                for capsule in capsules:
                    capsule.updateState()
            except Exception as e :
                TCommentsPipe.logger.error('WARNING, problem following up in the State Capsule')
                TCommentsPipe.logger.error(e)
                #TCommentsPipe.logger.warning(sys.exc_info()[0])
