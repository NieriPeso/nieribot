from pymongo import MongoClient
from decouple import config
import discord

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.time import get_date

# REMATES

def alargar_remate(id):
    pass

def terminar_remate(id):
    client = MongoClient(config('CONN_STR'))
    coll = client['nieribot']['remates']
    coll.update_one(
        {'ID': id},
        {'$set':{'activo':False}}
    )
    client.close()

def cantidad_remates():
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    return coll.count_documents({})+1

def obtener_datos(id):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    datos = coll.find_one({'ID': id})
    return datos

def obtener_remates_on():
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    datos = coll.find({'activo':True})
    client.close()
    return datos

def agregar_remate(remate):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    coll.insert_one(remate)
    client.close()

def guardar_puja(id, puja):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    coll.update_one(
        {'ID': id},
        {'$push': {'postores': puja}}
    )
    client.close()

def guardar_id_mensaje(msg_id):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    id = cantidad_remates() - 1
    coll.update_one(
        {'ID': id},
        {'$set': {'message_id': msg_id}}
    )
    client.close()

def add_picture(id, img):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    coll.update_one(
        { 'ID' : id },
        { 'foto' : img }
    )
    client.close()

# ========================================================================


# NUEVOS NIERIS

def nuevo_nieri(name, wallet):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
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