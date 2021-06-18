from pymongo import MongoClient
from decouple import config

def obtener_datos(id):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    datos = coll.find_one({'ID':id})
    return datos

def agregar_remate(remate, id):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    if coll.find_one({"ID":id}) == None:
        coll.insert_one(remate)
        client.close()
        return True
    client.close()
    return False

def guardar_puja(id, pujas):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    coll.update_one(
        {'ID': id},
        {'$set':{'Postores':pujas}}
    )