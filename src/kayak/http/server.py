#import user
import os
import tornado.ioloop #@UnresolvedImport
import tornado.web #@UnresolvedImport

#import md5
import logging
import datetime

import boobox.config
import boobox.kayak.http.request

settings = {
    "static_path": os.path.join(boobox.config.STATIC_CONTENT_LOCATION)
}

'''
    Sample call : http://localhost:6888/q?user=1217406&query=paris&access_token=139274172804886|a093abbd2e56a585884b2503-1217406|3ugNZ8Q9eheb01ty_jq1pUxih_M

'''
class AsyncQueryHandler(tornado.web.RequestHandler):

    # create logger
    logger = logging.getLogger("AsyncQueryHandlerLogger")
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
    
    def returnPartial(self, items, cursor=0, done=0):
        AsyncQueryHandler.logger.debug('returning partial')
        ret = {
                'cursor' : cursor + len(items),
                'items' : items,
                'done' : done
              }
        partial = { 'data' : ret}
        self.write(partial)
        self.finish()
    
    @tornado.web.asynchronous
    def get(self):
        self.set_header("Access-Control-Allow-Origin", boobox.config.ALLOW_ORIGIN)
        self.set_header("Content-Type", "application/json")
        self.set_status(200)    
        
        fbid = self.get_argument('facebook_id', None)
        cursor = int(self.get_argument('cursor', None))
        access_token = self.get_argument('access_token', None)

        if fbid == None or access_token == None:
            self.set_status(400)
            self.write('This request requires a user handle & an access token')
            self.finish()
        else :
            
            #####################################################
            ## Ideally everything under here, we should decouple#
            #####################################################
            boobox.kayak.http.request.execute(fbid=fbid, cursor=cursor, access_token=access_token, callback=self.returnPartial)

 
application = tornado.web.Application([
    (r"/q", AsyncQueryHandler),
], **settings)

if __name__ == "__main__":
    application.listen(6888)
    tornado.ioloop.IOLoop.instance().start()