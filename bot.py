import discord
from discord.ext import commands
from decouple import config
from utils.constants import *
from utils.messages import *
from commands import remates, nuevonieri, chat

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 852333212373745674:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

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

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    # (HAY QUE HACER EL FILTRO PARA LOS MODERADORES USAR SOLAMENTE)
    # if message.content.lower().startswith(clear_chat):
    #     await chat.limpiar_chat(message=message)

    if message.content.lower().startswith(nuevo_nieri):
        embed = nuevonieri.registro(message=message, name=message.author.name)
        await message.channel.send(embed=embed)

    # ============================== REMATE-VALORATE ==============================
    # COMANDO PARA PLANTARSE A UN REMATE
    if message.content.lower().startswith(puja) or message.content.startswith(oferta):
        if message.channel.id == 854807192997330944:
            embed, error = remates.pujar_remate(message=message)
            if not error:
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(embed=embed)

    # COMANDO PARA EL REGISTRO DE LOS REMATES
    # if message.content.lower().startswith(crear_remate):
    #     if message.channel.id == 854807192997330944:
    #         embed, error = remates.crear_remate(message=message)
    #         if not embed and not error:
    #             return
    #         if not error:
    #             channel = bot.get_channel(854807245509492808)
    #             await channel.send(embed=embed)
    #         else:
    #             await message.channel.send(embed=embed)

        # ===========================================================================

    # ESCUCHAR EL COMANDO '$nieripeso' EN CUALQUIER CANAL PARA ENVIAR INSTRUCCIONES POR PRIV.
    if message.content.lower().startswith(nieripeso):
        for msg in instrucciones:
            await message.author.send(msg)
        
@bot.command
async def send_help(ctx):
    await send_help()

# BORRADO DE 50 MENSAJES EN UN CANAL, SE PUEDE PASAR UN NUMERO
@bot.command(name='clear-chat')
async def limpieza(ctx, arg=None):
    await chat.limpiar_chat(ctx=ctx, arg=arg)

@bot.command(name='puja')
async def pujar(ctx, *args):
    pass
        
@bot.command(name='crear-remate')
async def crear(ctx, *args, **kwargs):
    if ctx.channel.id == 854807192997330944:
        if args or kwargs:
            embed, error = remates.crear_remate(message=ctx.message)

            if not embed and not error:
                return

            if error == 0:
                channel = bot.get_channel(854807245509492808)
                await channel.send(embed=embed)

            elif error == 1:
                await ctx.channel.send(embed=embed)
            
            elif error == 2:
                await ctx.channel.send(embed=embed)
                await ctx.send('$crear-remate\n*nombre ÑERIBOT\n*descripcion El bot de y para los ñeris\n*base 1000\n*final 20/04/22 16:20')

        else:
            await ctx.send('$crear-remate\n*nombre \n*descripcion \n*base \n*final')

# EJECUCIÓN DEL BOT
bot.run(config('TOKEN'))