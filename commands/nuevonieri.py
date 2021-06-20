import discord
from . import db

enable = False

def registro(message,  name):
    if enable:
        sep = message.content.split(' ')
        if len(sep) > 1:
            return db.nuevo_nieri(name=message.author.name, wallet=sep[1])

    else:
        embed = discord.Embed(
            title=f'LO SIENTO {name}',
            description=f'Esta feature esta desactivada',
            colour=discord.Color.orange()
        )
        return embed
