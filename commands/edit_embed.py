import discord

def edit_embed(data):
    embed = discord.Embed(
        title=f'{data["name"]}',
        description=f'{data["description"]}',
        colour=discord.Color.green()
    )
    embed.add_field(name='ID del remate:', value=f'{data["id"]}', inline=False)
    embed.add_field(name='Rematador:', value=f'<@{data["ownerId"]}>', inline=False)
    embed.add_field(name='Precio base:', value=f'{data["baseAmount"]}', inline=False)
    embed.add_field(name='Fecha de finalización:', value=f'{data["closeAt"]}', inline=False)
    embed.set_image(url=data["image"])
    text = ''
    if len(data['offers']) > 5:
        for x in range(len(data["offers"])-5, len(data["offers"])):
            text += f'{data["offers"][x]["createdAt"].strftime("%d/%m/%Y %H:%M")}\t' + '-\t' + f'<@{data["offers"][x]["bidderId"]}>\t' + '-\t' + f'<:nieripeso:852661603321249824>{str(data["offers"][x]["amount"])}' + '\n'
        embed.add_field(name='Últimos 5 postores:', value=text, inline=False)
    else:
        for p in data["offers"]:
            text += f'{p["createdAt"].strftime("%d/%m/%Y %H:%M")}\t' + '-\t' + f'<@{p["bidderId"]}>' + '-\t' + f'<:nieripeso:852661603321249824>{str(p["amount"])}' + '\n'
        embed.add_field(name='Postores:', value=text, inline=False)
    return embed
