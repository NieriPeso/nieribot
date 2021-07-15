from pymongo import MongoClient
from decouple import config
import discord

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# REMATES

def alargar_remate(id, new_close):
    client = MongoClient(config('CONN_STR'))
    coll = client['nierimarket']['sales']
    coll.update_one(
        {'id': id},
        {'$set':{'closeAt':new_close}}
    )
    client.close()

def close_remate(id, doc, _id):
    client = MongoClient(config('CONN_STR'))
    coll = client['nierimarket']['sales']
    coll.replace_one(
        {'id':id},
        doc,
        True
    )
    coll.delete_one({'_id':_id})
    client.close()

def terminar_remate(id):
    client = MongoClient(config('CONN_STR'))
    coll = client['nierimarket']['sales']
    coll.update_one(
        {'id': id},
        {'$set':{'active':False}}
    )
    client.close()

def cantidad_remates():
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    return coll.count_documents({})+1

def obtener_datos(id):
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    datos = coll.find_one({'id': int(id)})
    return datos

def obtener_remates_on():
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    datos = coll.find({'active':True})
    client.close()
    return datos

def agregar_remate(remate):
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    coll.insert_one(remate)
    client.close()

def guardar_puja(id, puja):
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    coll.update_one(
        {'id': id},
        {'$push': {'offers': puja}}
    )
    client.close()

def guardar_id_mensaje(msg_id):
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['sales']
    id = cantidad_remates() - 1
    coll.update_one(
        {'id': id},
        {'$set': {'messageId': msg_id}}
    )
    client.close()

# NUEVOS NIERIS

def nuevo_nieri(name, wallet):
    client = MongoClient(config('CONN_STR'))
    db = client['nierimarket']
    coll = db['nuevos_nieris']
    if coll.find_one({'Wallet': wallet}) == None:
        save = {
            'Discord_Name': name,
            'Wallet': wallet,
            'Entregado': {
                'ÑERIS': False,
                'BNB': False
            },
            'Veces': 1
        }
        coll.insert_one(save)
        client.close()
        embed = discord.Embed(
            title=f'{name} REGISTRADO',
            description='Has quedado registrado en la lista de espera, ten paciencia, son muchos nieris nuevos.\nGracias',
            colour=discord.Color.green()
        )
        return embed
    else:
        coll.update_one(
            {'Wallet': wallet},
            {'$inc': {'Veces':1}}
        )
        client.close()
        embed = discord.Embed(
            title=f'ATENCION {name}',
            description=f'Parece que esta wallet ya esta registrada, ten paciencia.',
            colour=discord.Color.red()
        )
        return embed

# ========================================================================