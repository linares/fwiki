'''
Created on Apr 29, 2011

@author: bigI
'''

import threading
from boobox.search.QueryRetriever import QueryRetriever

class QueryPipeline(threading.Thread):


    def __init__(self, capsule):
        self.__capsule = capsule
        super(QueryPipeline, self).__init__()
    
    def run(self):

        #Create query retreiever object
        query_retriever = QueryRetriever(self.__capsule.user().getIndexLocation())
        query_retriever.getEnv().attachCurrentThread()

        #Return docs
        docs = query_retriever.search(self.__capsule.query())

        #let the cursor handler figure out when to return
        self.__capsule.cursor_handler().addRawDocuments(docs)
        query_retriever.finish()