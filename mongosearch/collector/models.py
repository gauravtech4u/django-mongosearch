from mongosearch.core.connection import db

class CollectionWrapper( object ):
 
    def load_json( self, kwargs ):
        self.db_col.insert( kwargs )
    
    def find_one( self, kwargs ):
        return self.db_col.find_one( kwargs )
        
    def find( self, kwargs ):
        return self.db_col.find( kwargs )
        
    def save( self, kwargs ):
        self.db_col.find( kwargs )
        
    def update( self, find_dict, set_dict ):
        self.db_col.update( find_dict, set_dict )
        
    @classmethod 
    def collection_names( self ):
        return db.collection_names()
    
class CollectionMapping( CollectionWrapper ):

    def __init__( self, model ):
        self.db_col = db[model]
    
    def save( self, kwargs ):
        self.db_col.find( kwargs )
    
    
class CollectionContentType( CollectionWrapper ):    
    
    def __init__( self ):
        self.db_col = db['mongo_content']
        
    def collection_keys( self, collection_name ):
        self.db_col.find( {'collection_name':collection_name} ).key_names
        
