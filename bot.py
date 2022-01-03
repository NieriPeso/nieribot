import discord, requests, json, asyncio
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
from sockets.socket import SocketManager

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
bot = commands.Bot(command_prefix='$', help_command=None)

NIERI_GUILD = 847456853465497601

@bot.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 871171938964353095:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'nieripeso':
            role = discord.utils.get(guild.roles, name='ñeri')
        else:
            role = None

        if role is not None:
            member = payload.member
            if member is not None:
                await payload.member.add_roles(role)

@bot.event
async def on_message(message):
    if validate_channel(message.channel.id, key='cartelera-remates'):
        print(f"Message id de cartelera remates: {message.id}")
    await bot.process_commands(message)

    # LÓGICA PARA HACER QUE LOS MENSAJES DEL BOT NO SE ESCUCHEN
    if message.author == bot.user:
        return
    
    if type(message.channel) is discord.DMChannel and message.content.startswith('ANUNCIO:'):
        other_user = message.channel.recipient
        if NIERI_GUILD not in [g.id for g in other_user.mutual_guilds]: return
        nieri_guild = await bot.fetch_guild(NIERI_GUILD)
        nieri_member = await nieri_guild.fetch_member(other_user.id)
        if 'dev' in [r.name for r in nieri_member.roles]:
            nieri_chat = await nieri_guild.fetch_channel(915753815033131100)
            await nieri_chat.send('@everyone ' + message.content)

# COMANDO PARA ENVIAR INSTRUCCIONES DE COMO REGISTRARSE A UN NUEVI ÑERI
@bot.command(name=ñeripeso)
async def instrucciones_priv(ctx):
    for msg in instrucciones:
        await ctx.message.author.send(msg)

@bot.command(name=ir_al_super)
async def send_data(ctx):    
    headers = {
        "x-api-key": config('X-API-KEY')
    }

    body = {
        'id':ctx.message.author.id,
        'user':ctx.message.author.name,
        'photo':str(ctx.message.author.avatar_url),
        'roles': [role.name.lower() for role in ctx.message.author.roles]
    }

    req = requests.post('https://mercado.nieri.uy/api/auth/signIn', headers=headers, json=body)
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
    headers = { 'Content-Type': 'application/json' }
    response = requests.get('https://nieri.uy/api/cotization', headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    embed = discord.Embed(
        tittle='COTIZACIÓN',
        description=f'Pedido por parte de: {ctx.message.author.name}',
        color=discord.Color.gold()
    )
    embed.add_field(name=data['name'], value=data['value'])
    # comparationID = random.randint(1, 3)
    # price = random.randint(1, 999)
    # if comparationID == 3:
    #     embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {comparision[comparationID][random.randrange(0, len(comparision[comparationID]))]}')
    # elif comparationID == 2:
    #     embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {price} {comparision[comparationID][random.randrange(0, len(comparision[comparationID]))]}')
    # else:
    #     embed.add_field(name='Respuesta:', value=f'El <:nieripeso:852661603321249824> cotiza -> {comparision[comparationID][random.randrange(0, len(comparision[comparationID]))]} {price}')
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

# * EJECUCIÓN DEL BOT y del socket client (generando multhread event loop) 
loop = asyncio.get_event_loop()
loop.create_task(SocketManager.run())
loop.create_task(bot.run(config('TOKEN')))
loop.run_forever()
