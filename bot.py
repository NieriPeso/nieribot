from utils.bot_manager import BotManager
import discord
from discord.ext import commands
from decouple import config

from utils.constants import *
from utils.messages import *
from utils.time import end

from commands import chat, remates, nuevonieri, help, puja, chat
from commands.db import *

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
bot = commands.Bot(command_prefix='$', help_command=None)

class Nieribot(BotManager):
    bot = bot
    def ___init__(self, working_channel):
        self.workinChannel = working_channel
        super().__init__(self, working_channel)
    def run(self):
      # EJECUCIÓN DEL BOT
      self.bot.run(config('TOKEN'))   

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
        await bot.process_commands(message)        # LÓGICA PARA VER SI LOS REMATES ACTIVOS HAN TERMINADO
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
                channel = bot.get_channel(id=849410645513207828)
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
              
Nieri = Nieribot(working_channel = 829566898706317344)

# * Commands listeners definition
Nieri.use(
  'crear-remate', remates.crear_remate_command
).use(
  'ayuda', help.help_command
).use(
  'puja', puja.pujar_command
).use(
  'clear-chat', chat.limpiar_chat_command
).use(
  'nieripeso', chat.nieripeso_instrucciones_priv_command,
).use(
  'nuevonieri', nuevonieri.registro_nieri_command
)

Nieri.run()