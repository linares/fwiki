'''
Created on Aug 1, 2011

@author: bigI
'''

from django.core.management.base import BaseCommand, CommandError
from fwiki.taxonomy.bootstrap import FreebaseIndex
from fwiki.taxonomy.bootstrap.ImportToMySQL import MySQLNodeImporter

import os
import logging
import sys

from optparse import make_option

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--base-dir', '-b',
           dest='base_dir'
           ),
        make_option('--index', '-i',
           dest='index'
           ),
        make_option('--structure', '-s',
           dest='structure'
           ),
       )
    
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    
    # create logger
    logger = logging.getLogger("CreateTaxoCommand")
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

    TAXONOMY_RAW = 'raw_taxonomy'
    TAXONOMY_INDEX = 'index_taxonomy'
    

    def handle(self, *args, **options):
        sys.setdefaultencoding('iso-8859-1')
        reload(sys)
        
        
        taxonomy = {}
        
        BASE_DIR = options.get('base_dir')
        
        if not options.get('index') == None :
            Command.logger.debug('got index param')
        if not options.get('structure') == None :
            Command.logger.debug('got structure param')
            
        if BASE_DIR == None:
            raise CommandError('You need to provide a base directory where the taxonomy will be stored and indexed use --base-dir or -b')
            
        FreebaseIndex.buildTaxonomy(taxonomy, BASE_DIR + Command.TAXONOMY_RAW)
        
        if not options.get('index') == None :
            FreebaseIndex.indexTaxonomy(taxonomy, BASE_DIR + Command.TAXONOMY_INDEX)
            Command.logger.debug('--DONE INDEXING--')
        
        if not options.get('structure') == None :
            msni = MySQLNodeImporter()
            for node in taxonomy:
                msni.importNode(taxonomy[node])
        