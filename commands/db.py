from pymongo import MongoClient
from decouple import config
import discord
from datetime import datetime

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.time import get_date

# REMATES

# def comprobar_si_termino(id):
#     fecha_puja = get_date()
#     date = obtener_datos(id=id)['cierre']
#     date = datetime(day=int(date.split(' ')[0].split('/')[0]), month=int(date.split(' ')[0].split('/')[1]), year=int(date.split(' ')[0].split('/')[2]), hour=int(date.split(' ')[1].split(':')[0]), minute=int(date.split(' ')[1].split(':')[1]))
#     if (date-fecha_puja).days == 0:
#         # if int(fecha_puja[1].split(':')[0]) == int(date[1].split(':')[0]) and int(fecha_puja[1].split(':')[1]) >= int(date[1].split(':')[1]) - 5 and int(fecha_puja[1].split(':')[1]) <= int(date[1].split(':')[1]):
#         #     alargar_remate(id=id)
#         #     return False
#         if (fecha_puja-date).seconds <= 0:
#             terminar_remate(id=id)
#             return True
#         else:
#             return False
#     else:
#         return False

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