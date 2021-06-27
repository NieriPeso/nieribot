import discord

def unvailable(user):
    embed = discord.Embed(
        title='LO SIENTO',
        description=f'<@{user}> este comando está en construccion por el momento',
        colour=discord.Color.dark_orange()
    )
    return embed