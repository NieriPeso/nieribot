import discord
from discord.ext import commands
from decouple import config
from utils.constants import *
from utils.messages import *
from commands import remates, nuevonieri, chat
from commands.db import guardar_id_mensaje, obtener_remates_on, terminar_remate
from commands.help import *
from utils.time import get_date_future, end

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
        if end(remate['cierre']):
            terminar_remate(id=remate['ID'])
            # OBTENER CANAL DE CARTELERA Y EL MSG DEL REMATE FINALIZADO
            cartelera = bot.get_channel(id=854807245509492808)
            msg = await cartelera.fetch_message(remate['message_id'])
            history_channel = bot.get_channel(id=858860323850551337)
            embed = discord.Embed(
                title=f'{remate["nombre_rem"]}',
                description=f'{remate["descripcion_rem"]}',
                colour=discord.Color.dark_green()
            )
            embed.add_field(name='Rematador:', value=f'<@{remate["id_rematador"]}>', inline=False)
            embed.add_field(name='Precio base <:nieripeso:852661603321249824>:', value=f'{remate["base"]}', inline=False)
            if len(remate["postores"]) > 0:
                embed.add_field(name='Ganador:', value=f'<@{remate["postores"][-1][3]}>', inline=False)
                embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{remate["postores"][-1][2]}', inline=False)
            else:
                embed.add_field(name='Lo siento', value='Parece que nadie realizó una puja en tu remate', inline=False)
            if remate['foto'] != None:
                embed.set_image(url=remate['foto'])
            embed.set_footer(text='REMATE CERRADO')
            await history_channel.send(embed=embed)
            await msg.delete()

            # OBTENER CANAL DE REMATE-VALORATE PARA ENVÍAR AVISO
            channel = bot.get_channel(id=854807192997330944)
            emb = discord.Embed(
                title='UN REMATE LLEGÓ A SU CIERRE',
                description=f'Nombre: {remate["nombre_rem"]}\nID: {remate["ID"]}',
                colour=discord.Color.gold()
            )
            emb.add_field(name='REMATADOR:', value=f'<@{remate["id_rematador"]}>', inline=False)
            try:
                emb.add_field(name='GANADOR:', value=f'<@{remate["postores"][-1][3]}>', inline=False)
            except:
                emb.add_field(name='LO SIENTO', value='Parece que no hubo pujas en este remate', inline=False)
            await channel.send(embed=emb)

    # LÓGICA PARA HACER QUE LOS MENSAJES DEL BOT NO SE ESCUCHEN
    # A MENOS QUE SEA EN EL CANAL DE CARTELERA-REMATES PARA PODER
    # GUARDAR EL ID EN DB Y PODER EDITAR/BORRAR EL MENSAJE
    # CUANDO SE REQUIERA
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
@bot.command(name='clear-chat')
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
                if edit:
                    await ctx.send('$puja\n*id 1\n*Ñ 1000')
        else:
            await ctx.send('$puja\n*id \n*Ñ ')

# COMANDO PARA CREAR UN REMATE     
@bot.command(name='crear-remate')
async def crear(ctx, *args):
    if ctx.channel.id == 854807192997330944:
        if args:
            embed, error, confirm = remates.crear_remate(message=ctx.message)

            if not embed and not error:
                return

            if error == 0:
                channel = bot.get_channel(854807245509492808)
                await channel.send(embed=embed)
                await ctx.message.channel.send(embed=confirm)

            elif error == 1:
                await ctx.channel.send(embed=embed)
            
            elif error == 2:
                await ctx.channel.send(embed=embed)
                await ctx.send('$crear-remate\n*nombre ÑERIBOT\n*descripcion El bot de y para los ñeris\n*base 1000\n*final 20/04/22 16:20')

        else:
            await ctx.send(f'$crear-remate\n*nombre \n*descripcion \n*base \n*final {get_date_future()}')

# COMANDO DE AYUDA PARA USAR EL BOT
@bot.command(name=ayuda)
async def ayuda(ctx, *args):
    if not args:
        embed = unvailable(user=ctx.message.author.id)
    await ctx.send(embed=embed)

# EJECUCIÓN DEL BOT
bot.run(config('TOKEN'))