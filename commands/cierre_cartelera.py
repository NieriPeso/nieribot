from .db import terminar_remate
import discord

async def cierre(remate, cartelera, cartelera_cerrados, remate_valorate):
    terminar_remate(id=remate['id'])
    msg = await cartelera.fetch_message(remate['messageId'])
    embed = discord.Embed(
        title=f'{remate["name"]}',
        description=f'{remate["description"]}',
        colour=discord.Color.dark_green()
    )
    embed.add_field(name='Rematador:', value=f'<@{remate["ownerId"]}>', inline=False)
    embed.add_field(name='Precio base <:nieripeso:852661603321249824>:', value=f'{remate["baseAmount"]}', inline=False)
    if len(remate["offers"]) > 0:
        embed.add_field(name='Ganador:', value=f'<@{remate["offers"][-1]["bidderId"]}>', inline=False)
        embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{remate["offers"][-1]["amount"]}', inline=False)
    else:
        embed.add_field(name='Lo siento', value='Parece que nadie realizó una puja en tu remate', inline=False)
    embed.set_image(url=remate['image'])
    embed.set_footer(text='REMATE CERRADO')
    await cartelera_cerrados.send(embed=embed)
    await msg.delete()
    emb = discord.Embed(
        title='UN REMATE LLEGÓ A SU CIERRE',
        description=f'Nombre: {remate["name"]}\nID: {remate["id"]}',
        colour=discord.Color.gold()
    )
    emb.add_field(name='REMATADOR:', value=f'<@{remate["ownerId"]}>', inline=False)
    try:
        emb.add_field(name='GANADOR:', value=f'<@{remate["offers"][-1]["bidderId"]}>', inline=False)
    except:
        emb.add_field(name='LO SIENTO', value='Parece que no hubo pujas en este remate', inline=False)
    await remate_valorate.send(embed=emb)