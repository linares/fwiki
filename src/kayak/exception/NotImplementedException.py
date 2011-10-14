'''
Created on Mar 27, 2011

@author: bigI
'''

class NotImplementedException(Exception):
    '''
    classdocs
    '''

    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
