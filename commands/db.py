import pymongo
from pymongo import MongoClient
from decouple import config
from pymongo import collection

def remate_existente_check():
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    colection_remates = db['remates']

def agregar_remate(remate):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    collection = db['remates']
    collection.insert_one(remate)