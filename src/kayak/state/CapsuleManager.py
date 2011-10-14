'''
Created on May 2, 2011

@author: bigI
'''
import md5

class CapsuleManager(object):
    
    
    _instance = None
    _capsules = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CapsuleManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass
    
    '''
    {
        fb_id : {
            capsule_id : <capsule>,
            capsule_id : <capsule>
            capsule_id : <capsule>
            
        }
    }
    '''
    def addCapsule(self, capsule):
        fb_id = capsule.user().getId()
        if CapsuleManager._capsules.get(fb_id) :
            #we have a capsule being used by this user's query
            CapsuleManager._capsules.get(fb_id)[capsule.capsuleID()] = capsule
        else :
            #we have never seen this user before or there are no capsules in play
            CapsuleManager._capsules[fb_id] = {
                                                 capsule.capsuleID() : capsule
                                              }
    
    
    def capsulesForUser(self, fb_id):
        capsules = []
        cap_map = CapsuleManager._capsules.get(fb_id)
        
        for key in cap_map :
            capsules.append(cap_map[key])
        
        return capsules
    
    
    def removecapsule(self, capsule):
        fb_id = capsule.fbid()
        CapsuleManager._capsules.get(fb_id).pop(capsule.capsuleID(), None)
        