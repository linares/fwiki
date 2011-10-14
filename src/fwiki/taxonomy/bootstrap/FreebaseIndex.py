'''
Created on Jun 5, 2011

@author: bigI
'''





import logging
import os 
import pickle 
import pprint
import json
import sys

import fwiki.settings
import lucene
import freebase

from time import gmtime, strftime

from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexWriter, Version #@UnresolvedImport

reload(sys)
sys.setdefaultencoding('iso-8859-1')

TMP_PATH = '/tmp/'

GLOBAL_COUNT = 0

C_BY = '/location/location/containedby'
ID = 'id'
NAME = 'name'
ALIAS = '/common/topic/alias'
TYPE = 'type'
IMAGE = '/common/topic/image'

COUNTRY = '/location/country'
CONTINENT = '/location/continent'
CITY_TOWN = '/location/citytown'

IMG_URL_PREFIX = 'http://img.freebase.com/api/trans/raw'


# create logger
logger = logging.getLogger("FreebaseIndexer")
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

def queryCityTown(taxonomy, tourist_locations):
    logger.debug('queryCityTown')
    logger.debug(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
    
    query = [{ 
              "type": "/location/citytown", 
              "name": None,
              "id":None,
              "limit": 10,
              "/common/topic/alias": [],
              "/common/topic/image": [{
                                       "id": None, 
                                       "optional": True,
                                       "/common/image/size": {
                                                       "/measurement_unit/rect_size/x" : None,
                                                       "/measurement_unit/rect_size/y" : None
                                        }
                                     }] 
            }]
    
    if fwiki.settings.DEBUG == True:
        print 'in test mode'
        r = freebase.mqlread(query)
    else:
        print 'in production mode'
        count = 0
        while count < 3 :
            try:
                r = freebase.mqlreaditer(query)
                break
            except:
                count += 1
                
    for i in r:            
        buildTBranch(i,taxonomy,tourist_locations)

    
    
def queryDivisions(taxonomy, tourist_locations):
    logger.debug('queryDivisions')
    logger.debug(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
    query =[{
             "type":          "/location/administrative_division",
              "name":          None,
              "/common/topic/image" : [
                                       {
                                            "id": None,
                                            "optional" : True,
                                            "/common/image/size": {
                                                                   "/measurement_unit/rect_size/x" : None,
                                                                   "/measurement_unit/rect_size/y" : None
                                            }
                                        }
                                       ],
              "id":            None,
              "/common/topic/alias": [],
              "/location/location/containedby": [{
                "type":          "/location/country",
                "name":          None,
                "id":            None,
                "/common/topic/alias": [],
                "/location/location/containedby": [{
                  "type":          "/location/continent",
                  "optional":      True,
                  "name":          None,
                  "id":            None,
                  "/common/topic/alias": []
                }]
              }]
           }]
    count = 0
    
    if fwiki.settings.DEBUG == True:
        print 'in test mode'
        iter = freebase.mqlread(query)
    else:
        print 'in production mode'
        while count < 3 :
            try:
                iter = freebase.mqlreaditer(query)
                break
            except:
                count += 1
            
    for i in iter:
        contained_by = []
        for c in i[C_BY]:
            for cc in c[C_BY]:
                buildTBranch(cc, taxonomy, tourist_locations)
                contained_by.append(cc[NAME].lower())
                
            buildTBranch(c, taxonomy, tourist_locations, contained_by )
            contained_by.append(c[NAME].lower())
            
        buildTBranch(i,taxonomy,tourist_locations, contained_by)



def buildTBranch(item, taxonomy_ds, tourist_locations_ds, contained_by=[], godeep=True):
    t_node = taxonomy_ds.get(item[NAME].lower())
    if t_node == None:
        t_node = buildTNode(item, taxonomy_ds, tourist_locations_ds, contained_by, godeep)
        taxonomy_ds[item[NAME].lower()] = t_node



def buildTNode(node, taxonomy_ds, tourist_locations_ds, contained_by= [], godeep=True):
    global GLOBAL_COUNT
    global logger
    
    if GLOBAL_COUNT % 1000 == 0 :
        logger.debug(GLOBAL_COUNT)
    
    if godeep :
        if node[TYPE] == COUNTRY or node[TYPE] == CONTINENT or node[TYPE] == CITY_TOWN:
            tourist_locations_ds.append(node[NAME])
    
    TNode = {
      'id' : node[ID],
      'name' : unicode(node[NAME]),
      'alias' : [unicode(s.lower()) for s in node[ALIAS]],
      'type' : node[TYPE],
      'contained_by' : contained_by,
    }
    
    if not node.get(IMAGE) == None : 
        TNode['images'] = [{ "url" : IMG_URL_PREFIX + s['id'], "size" : s.get('/common/image/size') } for s in node[IMAGE]]
    else :
        TNode['images'] = [] 
    
    GLOBAL_COUNT = GLOBAL_COUNT + 1
    
    return TNode


'''
    Give it an empty taxonomy to fill
    Give it an empty tourist_locations to fill
'''
def buildTaxonomy(taxonomy, taxonomy_path):
    
    tourist_locations = []
    
    
    queryDivisions(taxonomy, tourist_locations)
    queryCityTown(taxonomy, tourist_locations)
    queryTouristAttractionsFor(taxonomy, tourist_locations)
    
    
    if os.path.exists(taxonomy_path):
        os.remove(taxonomy_path)
    
    f = open(taxonomy_path, 'w')
    
    pickle.dump(taxonomy, f)

def queryTouristAttractionsFor(taxonomy_ds, tourist_locations_ds):
    logger.debug('queryTouristAttractions')
    logger.debug(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
    queries = []
    
    print tourist_locations_ds
    
    BATCH = 300
    batch_size = 0
    for name in tourist_locations_ds:
        if batch_size == BATCH : #batch call for tourist attractions/travel destinations
            queryBatch(queries, taxonomy_ds)
            queries = []
            batch_size = 0 # reset
                        
        query = [{
                  "type":          "/travel/tourist_attraction",
                  "name":          None,
                  "id":             None,
                  "/location/location/containedby": name,
                  "/common/topic/alias" : [],
                  "/common/topic/image" : [
                                       {
                                            "id": None,
                                            "optional" : True,
                                            "/common/image/size": {
                                                   "/measurement_unit/rect_size/x" : None,
                                                   "/measurement_unit/rect_size/y" : None
                                            }
                                        }
                                       ],
                  }]
        queries.append(query)
        query = [{
                  "type":          "/travel/travel_destination",
                  "name":          None,
                  "id":             None,
                  "/location/location/containedby": name,
                  "/common/topic/alias" : [],
                  "/common/topic/image" : [
                                       {
                                            "id": None,
                                            "optional" : True,
                                            "/common/image/size": {
                                                       "/measurement_unit/rect_size/x" : None,
                                                       "/measurement_unit/rect_size/y" : None
                                            }
                                        }
                                       ],
                  }]
        queries.append(query)
        
        batch_size += 1
        
    
    if batch_size == BATCH : #batch call for tourist attractions/travel destinations
        queryBatch(queries, taxonomy_ds)
        queries = []
        batch_size = 0 # reset
    
    
    return [tourist_locations_ds]


def queryBatch(queries, taxonomy_ds):
    count = 0  #failure counter
    while count < 3 :
        try:
            attractions = freebase.mqlreadmulti(queries)
            break
        except:
            count += 1
    
    for top in attractions :
        if len(top) > 0 :
            for a in top:
                buildTBranch(a, taxonomy_ds, [] , [a[C_BY]], False)

def indexTaxonomy(taxonomy, index_path):
    lucene.initVM()
    
    index_location = index_path
    dir = SimpleFSDirectory(lucene.File(index_location))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    
    writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(1024))
    
    for i in taxonomy:
        v = taxonomy[i]
        doc = lucene.Document()
        doc.add(lucene.Field('name', v['name'] , lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('id', v['id'] , lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('alias', json.dumps(v['alias']) , lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('type', v['type'] , lucene.Field.Store.YES, lucene.Field.Index.NO))
        doc.add(lucene.Field('contained_by', json.dumps(v['contained_by']) , lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('images', json.dumps(v['images']) , lucene.Field.Store.YES, lucene.Field.Index.NO))
        writer.addDocument(doc)
        writer.commit()
        
    writer.close()




if __name__ == '__main__':
    
    
    taxonomy = {}
    
    buildTaxonomy(taxonomy, 'world_taxonomy')
    indexTaxonomy(taxonomy, 'taxo_index')



#def queryContinents():
#    query =[{
#             "type":          "/location/continent",
#              "name":          None,
#              "id":            None,
#              "/common/topic/image" : [
#                                       {
#                                            "id": None,
#                                            "optional" : True
#                                        }
#                                       ],
#              "/location/location/containedby": "Earth",
#              "/common/topic/alias": [],
#              "/location/location/contains": [{
#                "type": "/location/country",
#                "id":   None,
#                "name": None,
#                "/location/country/capital": [{
#                  "optional" : True,
#                  "name":          None,
#                  "id":            None,
#                  "/common/topic/alias": []
#                }]
#              }]
#            }]
#
#    return freebase.mqlreaditer(query)