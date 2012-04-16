from django.db.models import get_model


class Result(object):
    pass

class QuerySet(object):
    """A set of results returned from a query. Wraps a MongoDB cursor,
    providing :class:`~mongoengine.Document` objects as the results.
    """
    def __init__( self, db_col ):
        self.db_col=db_col
        
    
from django.db import models

class QuerySetManager(object):
    
    def __init__(self,db_col):
        self.db_col=db_col
        
    def filter(self,data):
        data_list=self.db_col.find( data )
        result_list = []
        for data_dict in data_list:
            obj=QuerySet(self.db_col)
            for col_name,col_value in data_dict.items():
                obj.__setattr__(col_name,col_value)
            result_list.append(obj)
        return result_list
    
    def all(self):
        data_list=self.db_col.find( {} )
        result_list = []
        for data_dict in data_list:
            obj=QuerySet(self.db_col)
            for col_name,col_value in data_dict.items():
                obj.__setattr__(col_name,col_value)
            result_list.append(obj)
        return result_list
    
    def get(self,data):
        obj=QuerySet(self.db_col)
        data_dict=self.db_col.find_one( data )
        result_list = []
        for col_name,col_value in data_dict.items():
            obj.__setattr__(col_name,col_value)
        result_list.append(obj)
        return result_list

    def update(self,key_dict,data_dict):
        self.db_col.update( key_dict , {"$set":data_dict} )