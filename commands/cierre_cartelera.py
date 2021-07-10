from .db import terminar_remate
import discord

async def cierre(remate, cartelera, cartelera_cerrados, remate_valorate):
    terminar_remate(id=remate['ID'])
    msg = await cartelera.fetch_message(remate['message_id'])
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
    await cartelera_cerrados.send(embed=embed)
    await msg.delete()
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
    await remate_valorate.send(embed=emb)