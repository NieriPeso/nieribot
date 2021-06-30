import discord
from utils.messages import instrucciones

async def limpiar_chat(ctx, arg):
    if "admins" in [y.name.lower() for y in ctx.author.roles] or "ñod" in [y.name.lower() for y in ctx.author.roles]:
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
    
    
async def limpiar_chat_command(bot_manager, ctx, arg=None):
    await limpiar_chat(ctx=ctx, arg=arg)


async def nieripeso_instrucciones_priv_command(bot_manager, ctx):
    for msg in instrucciones:
        await ctx.message.author.send(msg)
    