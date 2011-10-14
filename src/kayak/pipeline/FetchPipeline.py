'''
Created on Apr 3, 2011

@author: bigI
'''
import logging
import threading

#import pdb

from boobox.fetch.fb.fetchers.AlbumsFetcher import AlbumsFetcher

from boobox.search.AlbumsSearchAPI import AlbumsSearchAPI 

from boobox.kayak.pipeline.TCommentsPipe import TCommentsPipe
from boobox.kayak.pipeline.TPhotosPipe import TPhotosPipe
from boobox.kayak.pipeline.TAlbumsPipe import TAlbumsPipe
from boobox.kayak.state.CapsuleManager import CapsuleManager

class FetchPipeline(threading.Thread):
    
    # create logger
    #logger = logging.getLogger("FetchPipelineLogger")
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
        The fetch pipeline helps streamline everything that's needed to be fetched from FB and index on our side
        Kicks off : albums + photos followed incrementally by comments
    
    '''
    def __init__(self, capsule):
        self.__capsule = capsule
        self.__fetching_instances = 0
        self.__doneCondition = threading.Condition()
        super(FetchPipeline, self).__init__()
        #pdb.set_trace()
        
    def run(self):
        
        self.__fetching_instances = 1
        
        index_location = self.__capsule.user().getIndexLocation()
        token = self.__capsule.user().getAccessToken()
        
        #kick off album fetching
        albumsIndexer = AlbumsSearchAPI(index_location)
        albumsFetcher = AlbumsFetcher(token)
        albumThread = TAlbumsPipe(albumsFetcher, albumsIndexer, self.__capsule, self.__doneCondition, self.pipeIncremental)
        albumThread.start()
        
        thread_count = 0
        
        self.__doneCondition.acquire()
        while True:
            if thread_count < self.__fetching_instances:
                self.__doneCondition.wait()
            else:
                print 'CONDITION NOT MET'
                break
            
            thread_count += 1
            logging.debug('%(thread_count)d out of %(instances)d are done' , {'instances' : self.__fetching_instances, 'thread_count': thread_count})
        
        albumsIndexer.finish()
        logging.debug('ALL DONE')
        self.__doneCondition.release();

        #update the user record with what's been done
        self.__capsule.updateUser()
        capsules = CapsuleManager().capsulesForUser(self.__capsule.__user.getId())
        for capsule in capsules:
            capsule.closeCapsule()


    def chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
    
    '''
        this is pretty dirty for now : the callback from the albums TFetcher when we get a list of albums
        the idea is to kick off comments fetching/indexing once we get partial lists of albums
    '''
    def pipeIncremental(self, items, otherargs):
    
        chunks = list(self.chunks(items, 200))
        
        logging.debug(len(chunks))
        
        for chunk in chunks :
            logging.debug('comment chunk %(n)d' % {'n' : len(chunk) })
            #Get comments incrementally
            #commentsPipe = TCommentsPipe(self.__doneCondition, chunk, self.__capsule)
            #Get photos incrementally
            photosPipe = TPhotosPipe(self.__doneCondition, chunk, self.__capsule)
            self.__doneCondition.acquire()
            self.__fetching_instances += 1
            #commentsPipe.start()
            photosPipe.start()
            self.__doneCondition.release()
        
