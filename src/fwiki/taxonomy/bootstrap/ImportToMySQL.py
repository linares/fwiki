'''
Created on Aug 14, 2011

@author: bigI
'''

from fwiki.taxonomy.models import Node

import pickle
import sys

class MySQLNodeImporter(object):
    
    def __init__(self):
        pass
    
    def __transposeToNodeDAO(self, node):
        print node.get('name')
        return Node(name=node.get('name'), 
                    node_id=node.get('id'), 
                    type=node.get('type'),
                    alias=node.get('alias'),
                    contained_by=node.get('contained_by'),
                    images=node.get('images'))
    
    def importNode(self, node):
        n = self.__transposeToNodeDAO(node)
        n.save()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('iso-8859-1')
    
    
    taxo_location = '/tmp/world_taxonomy'
    
    f = open(taxo_location, 'rw')
    
    taxonomy = pickle.load(taxo_location)
    
    
    
    msni = MySQLNodeImporter()
    for node in taxonomy:
        msni.importNode(node)