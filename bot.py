import discord, random
from discord.ext import commands
from decouple import config
from utils.constants import *
from utils.messages import *
from commands import cierre_cartelera, remates, nuevonieri, chat
from commands.db import guardar_id_mensaje, obtener_remates_on
from commands.help import *
from utils.time import get_date_future, end
from commands.validation import validate_channel
from commands.get_channel_id import get_channel_id
from utils.fun import comparation

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

    # LÓGICA PARA VER SI LOS REMATES ACTIVOS HAN TERMINADO
    remates_on = obtener_remates_on()
    for remate in remates_on:
        if end(remate['closeAt']):
            cartelera = bot.get_channel(get_channel_id('cartelera-remates'))
            cartelera_cerrados = bot.get_channel(get_channel_id('cartelera-cerrados'))
            remate_valorate = bot.get_channel(get_channel_id('remate-valorate'))
            await cierre_cartelera.cierre(remate=remate, cartelera=cartelera, cartelera_cerrados=cartelera_cerrados, remate_valorate=remate_valorate)

    # LÓGICA PARA HACER QUE LOS MENSAJES DEL BOT NO SE ESCUCHEN
    # A MENOS QUE SEA EN EL CANAL DE CARTELERA-REMATES PARA PODER
    # GUARDAR EL ID EN DB Y PODER EDITAR/BORRAR EL MENSAJE
    # CUANDO SE REQUIERA
    if message.author == bot.user:
        if validate_channel(message.channel.id, key='cartelera-remates'):
            guardar_id_mensaje(msg_id=message.id)
        else:
            return

# COMANDO PARA REGISTRAR NUEVOSNIERIS Y SUS WALLETS PARA LA ENTREGA DE $Ñ
@bot.command(name=nuevo_nieri)
async def registro_nieri(ctx, wallet):
    embed = nuevonieri.registro(wallet=wallet, name=ctx.message.author.name)
    await ctx.send(embed=embed)

# COMANDO PARA ENVIAR INSTRUCCIONES DE COMO REGISTRARSE A UN NUEVI ÑERI
@bot.command(name=nieripeso)
async def instrucciones_priv(ctx):
    for msg in instrucciones:
        await ctx.message.author.send(msg)

# COMANDO PARA ENVIAR INSTRUCCIONES DE COMO REGISTRARSE A UN NUEVI ÑERI
@bot.command(name=ñeripeso)
async def instrucciones_priv(ctx):
    for msg in instrucciones:
        await ctx.message.author.send(msg)

# BORRADO DE 50 MENSAJES EN UN CANAL, SE PUEDE PASAR UN NUMERO
@bot.command(name=clear_chat)
async def limpieza(ctx, arg=None):
    await chat.limpiar_chat(ctx=ctx, arg=arg)

# COMANDO PARA PUJAR EN LOS REMATES
@bot.command(name=puja)
async def puja_rem(ctx, *args):
    if validate_channel(ctx.channel.id, key='remate-valorate'):
        if args:
            embed, error, edit, id_msg = remates.pujar_remate(message=ctx.message)
            if not error:
                channel = bot.get_channel(get_channel_id('cartelera-remates'))
                msg = await channel.fetch_message(id_msg)
                await chat.editar_msg_remate(message=msg, embed=edit)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed)
                if edit:
                    await ctx.send('$puja\n*id 1\n*Ñ 1000')
        else:
            await ctx.send('$puja\n*id \n*Ñ ')

# COMANDO PARA PUJAR EN LOS REMATES
@bot.command(name=pujar)
async def pujar_rem(ctx, *args):
    if validate_channel(ctx.channel.id, key='remate-valorate'):
        if args:
            embed, error, edit, id_msg = remates.pujar_remate(message=ctx.message)
            if not error:
                channel = bot.get_channel(get_channel_id('cartelera-remates'))
                msg = await channel.fetch_message(id_msg)
                await chat.editar_msg_remate(message=msg, embed=edit)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed)
                if edit:
                    await ctx.send('$pujar\n*id 1\n*Ñ 1000')
        else:
            await ctx.send('$pujar\n*id \n*Ñ ')

# COMANDO PARA CREAR UN REMATE
@bot.command(name=crear_remate)
async def crear(ctx, *args):
    if validate_channel(ctx.channel.id, key='remate-valorate'):
        if args:
            embed, error, confirm = remates.crear_remate(message=ctx.message)

            if not embed and not error:
                return

            if error == 0:
                channel = bot.get_channel(get_channel_id('cartelera-remates'))
                await channel.send(embed=embed)
                await ctx.message.channel.send(embed=confirm)

            elif error == 1:
                await ctx.channel.send(embed=embed)
            
            elif error == 2:
                await ctx.channel.send(embed=embed)
                await ctx.send('$crear-remate\n*nombre ÑERIBOT\n*descripcion El bot de y para los ñeris\n*base 1000\n*final 20/04/2022 16:20')

        else:
            await ctx.send(f'$crear-remate\n*nombre \n*descripcion \nRetiro: \n*base \n*final {get_date_future()}')

@bot.command(name=editar_remate)
async def edit(ctx):
    pass

@bot.command(name=cerrar_remate)
async def cierre(ctx, id, motive=None):
    if validate_channel(ctx.channel.id, key='remate-valorate'):
        embed = remates.cerrar_remate(ctx, id, motive)
        await ctx.channel.send(embed=embed)

@bot.command(name=blacklist)
async def mark_user(ctx, user_id):
    pass

@bot.command(name=ir_al_super)
async def send_data(ctx):
    import requests
    
    headers = {
        "x-api-key": config('X-API-KEY')
    }

    body = {
        'id':ctx.message.author.id,
        'user':ctx.message.author.name,
        'photo':str(ctx.message.author.avatar_url),
        'roles': [role.name.lower() for role in ctx.message.author.roles]
    }

    req = requests.post('https://mercado.nieri.uy/api/auth/signIn', headers=headers, data=body)
    data = req.json()
    
    embed = discord.Embed(
        title=f'{ctx.message.author.name}',
        description=f'[ABRIR EL SUPER](https://mercado.nieri.uy/?token={data["token"]})',
        colour=discord.Color.green()
    )

    await ctx.message.author.send(embed=embed)

# FUN COMMAND
@bot.command(name=cotizacion)
async def cotizar_nieri(ctx):
    comparationID = random.randint(1, 3)
    price = random.randint(1, 999)
    embed = discord.Embed(
        tittle='COTIZACIÓN',
        description=f'Pedido por parte de: {ctx.message.author.name}',
        color=discord.Color.gold()
    )
    if comparationID == 3:
        embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {comparation[comparationID][random.randrange(0, len(comparation[comparationID]))]}')
    elif comparationID == 2:
        embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {price} {comparation[comparationID][random.randrange(0, len(comparation[comparationID]))]}')
    else:
        embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {comparation[comparationID][random.randrange(0, len(comparation[comparationID]))]} {price}')
    await ctx.channel.send(embed=embed)

# COMANDO DE AYUDA PARA USAR EL BOT
@bot.command(name=ayuda)
async def help(ctx, *args):
    if not args:
        embed = unvailable(user=ctx.message.author.id)
    await ctx.send(embed=embed)

@bot.command(name=buscar_wallet)
async def busqueda(ctx, wallet):
    channel = bot.get_channel(854744124938387457)
    async for msg in ctx.channel.history(limit=None):
        if wallet in msg.content and not msg.content.startswith('$buscar-wallet '):
            embed = discord.Embed(
                title='USUARIO TURBIO',
                description=f'{msg.author.name}',
                colour=discord.Color.red()
            )
            embed.add_field(name='ID del user:', value=f'{msg.author.id}', inline=False)
            await channel.send(embed=embed)

# EJECUCIÓN DEL BOT
bot.run(config('TOKEN'))