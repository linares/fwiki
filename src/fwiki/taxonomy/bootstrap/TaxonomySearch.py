from lucene import QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, VERSION, initVM, Version  #@UnresolvedImport
import nltk
import sys

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        try:
            print
            print "Hit enter with no input to quit."
            command = raw_input("Query:")
            if command == '':
                return
    
            print
            print "Enter some text:", command
            
            #ngrams = get_nnp_ngrams(command)
            ngrams= []
            
            print ngrams
            
            if len(ngrams) > 0 :
                for ngram in ngrams:
                    print ngram
                    q = ' '.join(ngram)
                    print q
                    queryAndPrint(q)
                
            else:
                queryAndPrint(command)
            
                
        except Exception as e:
            print e
            
def queryAndPrint(query):
    query1 = QueryParser(Version.LUCENE_CURRENT, "name",
                        analyzer).parse("\"" + query + "\"")
    scoreDocs1 = searcher.search(query1, 1000).scoreDocs
    
    query2 = QueryParser(Version.LUCENE_CURRENT, "alias",
                        analyzer).parse("\"" + query + "\"")
    scoreDocs2 = searcher.search(query2, 1000).scoreDocs
    
    query3 = QueryParser(Version.LUCENE_CURRENT, "contained_by",
                        analyzer).parse("\"" + query + "\"")
    scoreDocs3 = searcher.search(query3, 1000).scoreDocs
    
    print "%s total matching documents." % (len(scoreDocs1) + len(scoreDocs2) + len(scoreDocs3))

    for scoreDoc in scoreDocs1:
        doc = searcher.doc(scoreDoc.doc)
        printStuff(doc)
            
    for scoreDoc in scoreDocs2:
        doc = searcher.doc(scoreDoc.doc)
        printStuff(doc)            
        
    for scoreDoc in scoreDocs3:
        doc = searcher.doc(scoreDoc.doc)
        printStuff(doc)

def printStuff(doc):
    name = None if doc.get("name") == None else doc.get("name").encode('utf-8')
    alias = None if doc.get("alias") == None else doc.get("alias").encode('utf-8')
    type = None if doc.get("type") == None else doc.get("type").encode('utf-8')
    id = None if doc.get("id") == None else doc.get("id").encode('utf-8')
    contained_by = None if doc.get("contained_by") == None else doc.get("contained_by").encode('utf-8')
    images = None if doc.get("images") == None else doc.get("images").encode('utf-8')
    
    print 'Item :', name, ' (alias:', alias , ')' , ' (type : ' , type, " )", ' (id : ' , id , " )", ' (contained by : ' , contained_by , " )", ' (images : ' , images , " )"
    
    
    
    
def get_nnp_ngrams(original_text, highlight=4, minsize=0):
    """
        Search @input orginial_text for ngrams of proper nouns 
        and return a list of relevant ngrams, read the comments
        above the function/method declaration as wo what each
        input does.
    """
    minsize = minsize-1
    if minsize<0:
        minsize = 0 
        
    tokens = nltk.wordpunct_tokenize(original_text)
    tagged = nltk.word_tokenize(original_text)
    tagged =  nltk.pos_tag(tokens)
    #for word in tagged:
    #   print word
    doc_length = len(tokens)
    counter = 0
    counter2 = 0
    if highlight==0:
        concated_test = doc_length # This is set to doc_length but could be anything recommend 3.
    else:
        concated_test = highlight
    list_of_NNPs = []
    while counter < (doc_length-1):
        while counter2 < concated_test:
            counter2 = counter2+1
            counter3 = 0
            #print '--------------------'
            temp_array = []
            all_nnp = True
            while counter3 < counter2:
                if counter < (doc_length-counter3):
                    #print tokens[counter+counter3],tagged[counter+counter3][1]
                    temp_array.append(tokens[counter+counter3])
                    if tagged[counter+counter3][1] != 'NNP':
                        all_nnp = False
                counter3 = counter3+1
            counter3 = 0
            if all_nnp == True:
                if(len(temp_array)>minsize):
                    list_of_NNPs.append(temp_array)
                #print 'added to main array'
            #else:
                #print 'not all NNPs'
        counter2 = 0
        counter = counter+1
    #for ngram in list_of_NNPs:
    #   print ngram
    import itertools
    list_of_NNPs.sort()
    unique_NNPs = list(list_of_NNPs for list_of_NNPs,_ in itertools.groupby(list_of_NNPs))
    return unique_NNPs    





     
if __name__ == '__main__':
    
    reload(sys)
    sys.setdefaultencoding('iso-8859-1')
    
    STORE_DIR = None
    while STORE_DIR == None:
        path = raw_input("What's the path to the index :")
        if path != '' and path != None :
            STORE_DIR = path
    
    initVM()
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    print searcher.maxDoc()
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    searcher.close()
