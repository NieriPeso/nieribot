from pymongo import MongoClient
from decouple import config
import discord
from datetime import datetime

# REMATES

def comprobar_si_termino(id):
    fecha_puja = datetime.now().strftime('%d/%m/%y %H:%M')
    fecha_puja = fecha_puja.split(' ')
    datos = obtener_datos(id=id)['Termina']
    datos = datos.split(' ')
    if int(fecha_puja[0].split('/')[0]) >= int(datos[0].split('/')[0]) and int(fecha_puja[0].split('/')[1]) >= int(datos[0].split('/')[1]) and int(fecha_puja[0].split('/')[2]) >= int(datos[0].split('/')[2]):
        if int(fecha_puja[1].split(':')[0]) >= int(datos[1].split(':')[0]) and int(fecha_puja[1].split(':')[1]) >= int(datos[1].split(':')[1]):
            terminar_remate(id=id)
            return True
        else:
            return False
    else:
        return False

def terminar_remate(id):
    client = MongoClient(config('CONN_STR'))
    coll = client['nieribot']['remates']
    coll.update_one(
        {'ID': id},
        {'$set':{'Activo':False}}
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
    terminada = comprobar_si_termino(id)
    if not terminada:
        client = MongoClient(config('CONN_STR'))
        db = client['nieribot']
        coll = db['remates']
        coll.update_one(
            {'ID': id},
            {'$push': {'Postores': puja}}
        )
        client.close()
        return True
    else:
        return False

def guardar_id_mensaje(id_msg_rem):
    client = MongoClient(config('CONN_STR'))
    db = client['nieribot']
    coll = db['remates']
    id = cantidad_remates()
    coll.update_one(
        {'ID': id},
        {'$set': {'id_msg_rem': id_msg_rem}}
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