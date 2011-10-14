import logging
import datetime

import boobox
import boobox.config

from boobox.kayak.state.StateCapsule import StateCapsule
from boobox.kayak.pipeline.FetchPipeline import FetchPipeline
from boobox.kayak.pipeline.QueryPipeline import QueryPipeline
from boobox.kayak.dal.Read import ReadDAL
from boobox.kayak.dal.Write import WriteDAL
from boobox.kayak.dao.UserDAO import User
from boobox.kayak.state.CursorHandler import CursorHandler
from boobox.search.QueryRetriever import QueryRetriever
from boobox.kayak.state.QueryWaiter import QueryWaiter
from boobox.kayak.state.CapsuleManager import CapsuleManager


def execute(**kwargs):
    fbid = kwargs.get('fbid')
    cursor = kwargs.get('cursor')
    access_token = kwargs.get('access_token')
    callback = kwargs.get('callback')

    logging.info("QUERY REQUEST %s %s ", fbid,cursor)

    if user == None :

        # Create/save user if does exist
        wdal = WriteDAL()
        user = User(fbid)
        user.setIndexTime(datetime.datetime.now().isoformat())
        user.setCreated(datetime.datetime.now().isoformat())
        user.setIndexing(1)
        user.setAccessToken(access_token)
        wdal.persistUser(user)

        #Prep user account (create index location, etc)
        user.prepFirstUse()

        #handles getting search hits when we get them and returning with partial results
        qw = QueryWaiter(callback, cursor, search_id)
        qw.start()

        #create capsule
        capsule = StateCapsule(cursor_handler=CursorHandler(cursor=cursor,searchid=search_id,callback=callback), query=query, user=user)
        CapsuleManager().addCapsule(capsule)

        #start fetch pipeline
        fp = FetchPipeline(capsule)
        #AsyncQueryHandler.logger.debug('FULL INDEXING CYCLE STARTED')
        fp.start()

    else :
        #this is a returning user
        #check to see if this user has already searched for this id (memcache)

        search_result = rdal.getSearchID(search_id)

        if search_result != None :
            #This is an existing query from the user that we still have in the cache
            #return the next page of results
            r = CursorHandler.getPageForSearchResults(search_result, cursor)

            if user.getIndexing() == 0:
                #this signifies we really have no more results to return
                callback(r, cursor, 1)
            else :
                #handles getting search hits when we get them and returning with partial results
                qw = QueryWaiter(callback, cursor, search_id)
                qw.start()

                #also need to kick off a query pipeline here so we start getting results asap
        else :
            qw = QueryWaiter(callback, cursor, search_id)
            qw.start()

            #brand new query for an existing user
            capsule = StateCapsule(cursor_handler=CursorHandler(cursor=cursor,searchid=search_id,callback=callback), query=query, user=user)
            CapsuleManager().addCapsule(capsule)
            qr = QueryPipeline(capsule)
            qr.start()


        #check the index time.  if the latest time we've queried this user's data is > THRESHOLD , kick off fetching + indexing from a certain point in time