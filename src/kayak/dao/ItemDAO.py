'''
Created on Apr 12, 2011

@author: bigI
'''


class Item(object):
    '''
    classdocs
    '''
    __tablename__ = 'booboxapp_userindex'
    
#    object_id = Column(String(128))
#    viewer_fbid = Column(Integer, primary_key=True)
#    type = Column(String(16))
#    data = Column(text)

    def __init__(self, object_id, fbid, type, data):
        self.object_id = object_id
        self.viewer_fbid = fbid
        self.type = type
        self.data = data
            
    
    def __repr__(self):
        return "<Item('%s','%d', '%s, %s')>" % (self.object_id, self.viewer_fbid, self.type, self.data)
    
    def getObjectId(self):
        return self.object_id
    
    def getData(self):
        return self.data
    
    def getType(self):
        return self.type