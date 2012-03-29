from mongosearch.search.genericsearch import MongoSearch

def  criteria( request ):
    obj = MongoSearch( request ).criteria()
    return obj

def  get_keys( request ):
    obj = MongoSearch( request ).get_keys()
    return obj

def filter_results( request ):
    obj = MongoSearch( request ).filter_results()
    return obj
