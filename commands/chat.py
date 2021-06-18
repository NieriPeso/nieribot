import discord

async def limpiar_chat(message):
    if "admins " in [y.name.lower() for y in message.author.roles] or "ñod" in [y.name.lower() for y in message.author.roles]:
        listamsg = message.content.split(" ")
        if len(listamsg) > 1:
            await message.channel.purge(limit=int(listamsg[1]))
        else:
            await message.channel.purge(limit=50)
        return None
    else:
        embed = discord.Embed(
            title='ERROR DE PERMISOS',
            description=f'{message.author.name}, debes tener el rol de "Admins" o "ñod" para usar este comando.',
            colour=discord.Color.orange()
        )
        return embed
