from pymongo import Connection

connection = Connection( 'localhost', 27017 )

db = connection.test_database
