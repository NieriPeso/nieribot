import discord
from discord import colour
from discord.ext import commands
from decouple import config
from utils.constants import *
from utils.messages import *
from commands import remates, nuevonieri, chat
from commands.db import guardar_id_mensaje

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
bot = commands.Bot(command_prefix='$', help_command=None)

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
        else:
            role = None

        if role is not None:
            member = payload.member
            if member is not None:
                await payload.member.add_roles(role)

@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author == bot.user:
        if message.channel.id == 854807245509492808:
            guardar_id_mensaje(msg_id=message.id)
        else:
            return

# COMANDO PARA REGISTRAR NUEVOSNIERIS Y SUS WALLETS PARA LA ENTREGA DE $Ñ
@bot.command(name='nuevonieri')
async def registro_nieri(ctx, wallet):
    embed = nuevonieri.registro(wallet=wallet, name=ctx.message.author.name)
    await ctx.send(embed=embed)

# COMANDO PARA ENVIAR INSTRUCCIONES DE COMO REGISTRARSE A UN NUEVI ÑERI
@bot.command(name='nieripeso')
async def instrucciones(ctx):
    for msg in instrucciones:
        ctx.message.author.send(msg)

# BORRADO DE 50 MENSAJES EN UN CANAL, SE PUEDE PASAR UN NUMERO
@bot.command(name='clear-chat', cog='Administración')
async def limpieza(ctx, arg=None):
    await chat.limpiar_chat(ctx=ctx, arg=arg)

# COMANDO PARA PUJAR EN LOS REMATES
@bot.command(name='puja')
async def pujar(ctx, *args):
    if ctx.message.channel.id == 854807192997330944:
        if args:
            embed, error, edit, id_msg = remates.pujar_remate(message=ctx.message)
            if not error:
                channel = bot.get_channel(854807245509492808)
                msg = await channel.fetch_message(id_msg)
                await chat.editar_msg_remate(message=msg, embed=edit)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed)
        else:
            await ctx.send('$puja\n*id \n*Ñ ')

# COMANDO PARA CREAR UN REMATE     
@bot.command(name='crear-remate')
async def crear(ctx, *args):
    if ctx.channel.id == 854807192997330944:
        if args:
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

# COMANDO DE AYUDA PARA USAR EL BOT
@bot.command(name='ayuda')
async def ayuda(ctx, *args):
    embed = discord.Embed(
        title='LO SIENTO',
        description='Este comando está en construccion',
        colour=discord.Color.dark_theme()
    )
    await ctx.send(embed=embed)

# EJECUCIÓN DEL BOT
bot.run(config('TOKEN'))