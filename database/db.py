from tinydb import TinyDB, Query
from tinydb.database import Document
from pprint import pprint
import json
User = Query()

db1=TinyDB('database/users.json', indent=4)
db2=TinyDB('database/medias.json', indent=4)
products  = db2.table('media') 

users     = db1.table('Users')
index     = db1.table('Index')

def get(table=None, user_id=None, media_id=None, uniq_id=None):


    if table == "users":
        if user_id != None:
            return users.get(doc_id=user_id)
        else:
            return False
    if table == "all_users":
        # print(users.all())
        return index
        
    elif table == "index":
        return index.get(doc_id=user_id)
    
    elif table == "media":
        try:
            ret = db2.get(doc_id=media_id)
            len_loads = ret["loads"]
            upd(table="media", media=int(media_id), data={"loads": int(len_loads + 1)})
            return ret
        except:
            return []
    
    elif table == "medias":
        return db2.all()
    
def insert(table, data, user_id=None, media_type=None):
    if table == "users":
        doc = Document(
            value=data,
            doc_id=user_id
        )
        users.insert(doc)
    
    elif table == "index":
        doc = Document(
            value=data,
            doc_id=user_id
        )
        index.insert(doc)

    elif table == "media":
       doc_id = db2.insert(data)
       return doc_id
    
def upd(table, data, user_id=None, media=None):

    if table == "index":
        index.update(data, doc_ids=[user_id])
    if table == "media":
        db2.update(data, doc_ids=[media])
    
def delete(media_id):
    try:
        db2.remove(doc_ids=[media_id])
        return True
    except:
        return False