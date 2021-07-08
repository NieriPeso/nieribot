import discord
from .validation import validate_permissions

async def limpiar_chat(ctx, arg):
    if validate_permissions(ctx):
        if arg == None:
            await ctx.channel.purge(limit=50)
        else:
            await ctx.channel.purge(limit=int(arg))
    else:
        embed = discord.Embed(
            title='ERROR DE PERMISOS',
            description=f'{ctx.author.name}, debes tener el rol de "Admins" o "ñod" para usar este comando.',
            colour=discord.Color.orange()
        )
        await ctx.channel.send(embed=embed)

async def editar_msg_remate(message, embed):
    await message.edit(embed=embed)