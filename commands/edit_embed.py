import discord

def edit_embed(data):
    embed = discord.Embed(
        title=f'{data["nombre_rem"]}',
        description=f'{data["descripcion_rem"]}',
        colour=discord.Color.green()
    )
    embed.add_field(name='ID del remate:', value=f'{data["ID"]}', inline=False)
    embed.add_field(name='Rematador:', value=f'<@{data["id_rematador"]}>', inline=False)
    embed.add_field(name='Precio base:', value=f'{data["base"]}', inline=False)
    embed.add_field(name='Fecha de finalización:', value=f'{data["cierre"]}', inline=False)
    if data["foto"] != None:
        embed.set_image(url=data["foto"])
    else:
        embed.add_field(name='Imagen:', value='NO HAY IMAGEN DEL REMATE', inline=False)
    text = ''
    if len(data['postores']) > 5:
        for x in range(len(data["postores"])-5, len(data["postores"])):
            text += f'{data["postores"][x][0]}\t' + '-\t' + f'<@{data["postores"][x][3]}>\t' + '-\t' + f'<:nieripeso:852661603321249824>{str(data["postores"][x][2])}' + '\n'
        embed.add_field(name='Últimos 5 postores:', value=text, inline=False)
    else:
        for p in data["postores"]:
            text += f'{p[0]}\t' + '-\t' + f'<@{p[3]}>' + '-\t' + f'<:nieripeso:852661603321249824>{str(p[2])}' + '\n'
        embed.add_field(name='Postores:', value=text, inline=False)
    return embed
