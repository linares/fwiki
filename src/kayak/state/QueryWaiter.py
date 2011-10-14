'''
Created on May 1, 2011

@author: bigI
'''
import threading
from boobox.kayak.state.ResultNotifier import ResultNotifier
from boobox.kayak.state.CursorHandler import CursorHandler

class QueryWaiter(threading.Thread):

    def __init__(self, cb, cursor, search_id):
        self.__cursor = cursor
        self.__cb = cb
        self.__waitCondition = threading.Condition()
        self.__results = []
        self.__resultNotifier = ResultNotifier()
        self.__search_id = search_id
        super(QueryWaiter, self).__init__()
        
    def run(self):
        
        self.__resultNotifier.waitForSearchResult(self.__search_id, self.cbOnQueryResults)
        self.__waitCondition.acquire()
        while True:
            if len(self.__results) <= self.__cursor :
                self.__waitCondition.wait()
            else:
                break
            
        self.__waitCondition.release()
        
        self.__resultNotifier.removeSearchResult(self.__search_id)
        try:
            self.__cb(CursorHandler.getPageForSearchResults(self.__results, self.__cursor), self.__cursor)
        except Exception as e :
            pass
            
    def cbOnQueryResults(self, results):
        self.__results = results
        self.__waitCondition.acquire()
        self.__waitCondition.notify()
        self.__waitCondition.release()    