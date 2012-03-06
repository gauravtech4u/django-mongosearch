from mongosearch.collector.mongodb import CreateMongoCollection

def  upload_form( request ):
    obj = CreateMongoCollection( request ).upload_form()
    return obj

def  create_db( request ):
    obj = CreateMongoCollection( request ).create_db()
    return obj
