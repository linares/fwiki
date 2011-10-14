'''
Created on Aug 14, 2011

@author: bigI
'''

from django.core.management.base import BaseCommand, CommandError
from fwiki.taxonomy.bootstrap.ImportToMySQL import MySQLNodeImporter
from fwiki.taxonomy.models import Node

import os
import logging
import pickle
import json
import sys

from optparse import make_option

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
       make_option('--taxo-file', '-f',
          dest='taxo_file'
          ),
      )

    args = '<taxo_dir>'
    help = 'imports the taxonomy pickled at the specified file into mysql'
    
    # create logger
    logger = logging.getLogger("ImportTaxoCommand")
    logger.setLevel(logging.DEBUG)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s")
    
    # add formatter to ch
    ch.setFormatter(formatter)
    
    # add ch to logger
    logger.addHandler(ch)
    
    
    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('iso-8859-1')
        
        path = options.get('taxo_file')
        
        if path == None:
            raise CommandError('You need to provide the taxonomy file path --taxo-file or -f')
    
        f = open(path, 'rw')
        
        
        
        #first delete all nodes
        Node.objects.all().delete()
        
        taxonomy = pickle.load(f)
        
        msni = MySQLNodeImporter()
        for i in taxonomy:
            count = 0
            while count < 3 :
                try:
                    msni.importNode(taxonomy[i])
                    break
                except:
                    count += 1 
                    Command.logger.error('could not import :' . taxonomy[i])
            if count == 3 :
                Command.logger.warning('skipping node '  . taxonomy[i])
                
        