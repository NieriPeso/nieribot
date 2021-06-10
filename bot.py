import discord
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {client.user}')

# TESTEO EN ESCUCHAR LAS REACCIONES
# FUNCIONA HASTA EL PUNTO QUE TOMA AL MIEMBRO PARA AGREGARLE ROL
# SI VEN ESTE CÓDIGO Y SABEN QUE LE PASA ME ESCRIBEN POR DISCORD
# MI USER EN DISCORD ES: '8ry4n'

# @client.event
# async def on_raw_reaction_add(payload):
#     if payload.message_id == 852333212373745674:
#         guild_id = payload.guild_id
#         guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
#         print('Guild: ', guild.members)
        
#         if payload.emoji.name == 'acepto':
#             role = discord.utils.get(guild.roles, name='nieris')
#             print(f'Role: {role}')
#         else:
#             role = None
#             print('Other emoji added')

#         if role is not None:
#             member = client.get_user(payload.user_id)
#             if member is not None:
#                 await member.add_roles(role)
#                 print('Rol agregado, nuevo nieri')
#             else:
#                 print('Member not found.')
#         else:
#             print('Role not found')

# @client.event
# async def on_raw_reaction_remove(payload):
#     if payload.message_id == 852333212373745674:
#         print(payload.emoji.name)

#         guild_id = payload.guild_id
#         guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
#         role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

#         if role is not None:
#             member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
#             await member.remove_roles(role)
#             print("done")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$nieripeso'):
        await message.channel.send('***TODAS LAS INSTRUCCIONES***!')

client.run('ODUxMTQyNDM3ODMyNjIyMTAx.YLz-Kg.KKWvFx-skDJeCnNqWwSl2sQqm4E')

#https://discord.com/api/oauth2/authorize?client_id=851142437832622101&permissions=8&scope=bot