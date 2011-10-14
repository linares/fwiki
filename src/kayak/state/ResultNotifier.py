'''
Created on May 1, 2011

@author: bigI
'''


class ResultNotifier(object):

    _instance = None
    _waitingConsumers = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResultNotifier, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass
        
    def waitForSearchResult(self, search_id, conditionCB):
        ResultNotifier._waitingConsumers[search_id] = conditionCB
        
    def removeSearchResult(self, search_id):
        ResultNotifier._waitingConsumers.pop(search_id, None)
    
    def notifyConditionWithResults(self, search_id, results):
        waitingCB = ResultNotifier._waitingConsumers.get(search_id)
        if waitingCB != None:
            waitingCB(results)
    
    def getAwaitingNotificationItems(self):
        return ResultNotifier._waitingConsumers
    
    
    
if __name__ == '__main__':
    s1=ResultNotifier()
    s1.notifyConditionForSearch('search1', 'bla')
    s2=ResultNotifier()
    s2.notifyConditionForSearch('search2', 'bla')
    
    if(id(s1)==id(s2)):
        print "Same"
    else:
        print "Different"
        
    print s2.getAwaitingNotificationItems()
    print s1.getAwaitingNotificationItems()