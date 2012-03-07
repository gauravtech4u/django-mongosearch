from mongosearch.core.connection import db


class CollectionWrapper(object):
 
    def load_json(self,kwargs):
        self.db_col.insert(kwargs)
    
    def find_one(self,kwargs):
        return self.db_col.find_one(kwargs)
        
    def find(self,kwargs):
        return self.db_col.find(kwargs)
        
    def collection_names(self,kwargs):
        return self.db_col.collection_names(kwargs)
    
    def save(self,kwargs):
        self.db_col.find(kwargs)
    
class CollectionMapping(CollectionWrapper):

    def __init__(self,model):
        self.db_col = db[model]
    
