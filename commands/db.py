from pymongo import MongoClient
from decouple import config
import discord
from datetime import datetime

# REMATES

def comprobar_si_termino(id):
    fecha_puja = datetime.now().strftime('%d/%m/%y %H:%M')
    datos = obtener_datos(id=id)

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
        {'$push': {'Postores': puja}}
    )

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
        embed = discord.Embed(
            title=f'ATENCION {name}',
            description=f'Parece que esta wallet ya esta registrada, ten paciencia.',
            colour=discord.Color.red()
        )
        return embed

# ========================================================================