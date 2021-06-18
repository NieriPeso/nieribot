import discord
from discord.ext import commands
from decouple import config
from utils.constants import *
from utils.messages import *
from commands import remates, nuevonieri, chat

# ESTRUCTURA DE COMANDOS Y ACCIONES DEL BOT

client = commands.Bot(command_prefix='/')

# INICIO DEL BOT PARA SU FUNCIONAMIENTO


@client.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {client.user}')


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 852333212373745674:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'acepto':
            role = discord.utils.get(guild.roles, name='nieri')
            #print(f'Role: {role}')
        else:
            role = None
            #print('Otro emoji agregado')

        if role is not None:
            member = payload.member
            if member is not None:
                await payload.member.add_roles(role)
                #print('Rol agregado, nuevo nieri')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # BORRADO DE 50 MENSAJES EN UN CANAL (HAY QUE HACER EL FILTRO PARA LOS MODERADORES USAR SOLAMENTE)
    if message.content.lower().startswith(clear_chat):
        await chat.limpiar_chat(message=message)

    if message.content.lower().startswith(nuevo_nieri):
        embed = nuevonieri.registro(message=message, name=message.author.name)
        await message.channel.send(embed=embed)

    # ============================== REMATE-VALORATE ==============================

    # COMANDO PARA PLANTARSE A UN REMATE
    if message.content.lower().startswith(puja) or message.content.startswith(oferta):
        embed, error = remates.pujar_remate(message=message)
        if not error:
            channel = client.get_channel(855566924711985192)
            await channel.send(embed=embed)
        else:
            await message.channel.send(embed=embed)

    # COMANDO PARA EL REGISTRO DE LOS REMATES
    if message.content.lower().startswith(crear_remate):
        embed, error = remates.crear_remate(message=message)
        if not error:
            channel = client.get_channel(855566924711985192)
            await channel.send(embed=embed)
        else:
            await message.channel.send(embed=embed)
        

        # ===========================================================================

    # ESCUCHAR EL COMANDO '$nieripeso' EN CUALQUIER CANAL PARA ENVIAR INSTRUCCIONES POR PRIV.
    if message.content.lower().startswith(nieripeso):
        for msg in instrucciones:
            await message.author.send(msg)


# EJECUCIÓN DEL BOT
client.run(config('TOKEN'))
