import discord
from . import db

enable = False

def registro(wallet,  name):
    if enable:
        return db.nuevo_nieri(name=name, wallet=wallet)

    else:
        embed = discord.Embed(
            title=f'LO SIENTO {name}',
            description=f'Esta feature esta desactivada',
            colour=discord.Color.orange()
        )
        return embed
