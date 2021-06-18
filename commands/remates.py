import discord, json
from datetime import datetime

def crear_remate(message):
    try:
        remate = message.content.lower()
        datos = remate.split('*')

        id_remate = str(datos[1][3:])
        rematador = str(message.author.name)
        remate_nombre = str(datos[2][7:])
        remate_descripcion = str(datos[3][12:])
        base = datos[4][5:]
        if len(datos[5]) > 6:
            final = str(datos[5][6:])
        else:
            embed = discord.Embed(
                title='ERROR',
                description='Es obligatorio escribir la fecha',
                colour=discord.Color.red()
            )
            return embed, True
        try:
            img = message.attachments[0].url
        except:
            img = None

        # CONVERTIR PRECIO A NUMERO ENTERO
        try:
            base = int(base)
        except ValueError:
            base = 0

        # ESCRIBIR A ARCHIVO CON REMATES
        file = open('remates.json', 'r')
        temp = json.load(file)
        file.close()
        temp[id_remate.replace('\n', '')] = {
            'Rematador': rematador,
            'Nombre de remate': remate_nombre.replace('\n', ''),
            'Descripcion del remate': remate_descripcion.replace('\n', ''),
            'Base': base,
            'Comienzo': datetime.now().strftime('%d/%m/%y %H:%M'),
            'Activo': True,
            'Termina': final.replace('\n', ''),
            'Postores': []
        }
        file = open('remates.json', 'w')
        json.dump(temp, file, indent=2)
        file.close()

        embed = discord.Embed(
            title=f'Nuevo remate con id {id_remate}',
            description=f'{remate_descripcion}',
            colour=discord.Color.green()
        )
        embed.add_field(name='Rematador:', value=f'{rematador}', inline=False)
        embed.add_field(name='Nombre del remate:',
                        value=f'{remate_nombre}', inline=False)
        embed.add_field(name='Precio base:', value=f'{base}', inline=False)
        embed.add_field(name='Fecha de finalización:',
                        value=f'{final}', inline=False)
        if not img == None:
            embed.set_image(url=img)
        else:
            embed.add_field(
                name='Imagen:', value='NO HAY IMAGEN DEL REMATE', inline=False)
        embed.set_footer(text='SUERTE A TODOS')

        return embed, False
    except:
        embed = discord.Embed(
            title='ERROR CREANDO REMATE',
            description=f'Lo siento {message.author.name} pero tu remate no pudo registrarse, algo esta mal.\nComprueba como escribiste el comando y corrígelo o pidele ayuda a un mod.',
            colour=discord.Color.red()
        )
        return embed, True

def pujar_remate(message):
    try:
        apuesta = message.content.lower()
        datos = apuesta.split('*')

        id_rem_apostar = str(datos[1][3:]).replace('\n', '')
        cantidad = int(datos[2][2:].replace('\n', ''))
        apuesta = [message.author.name, cantidad]

        file = open('remates.json', 'r')
        temp = json.load(file)
        file.close()

        postores = temp[id_rem_apostar]['Postores']
        if postores == [] and cantidad > temp[id_rem_apostar]['Base'] or postores[-1][1] < cantidad:
            postores.append(apuesta)

            temp[id_rem_apostar]['Postores'] = postores

            file = open('remates.json', 'w')
            json.dump(temp, file, indent=2)
            file.close()

            embed = discord.Embed(
                title=f'**Nueva puja al remate con id {id_rem_apostar}**',
                description=f'Este remate fue abierto por **{temp[id_rem_apostar]["Rematador"]}**',
                colour=discord.Color.green()
            )
            embed.set_author(name=f'{message.author.name}',
                            icon_url=f'{str(message.author.avatar_url)[:-4]}128')
            embed.add_field(name='Cantidad:', value=f'{cantidad}', inline=False)

            return embed, False
        else:
            embed = discord.Embed(
            title='ERROR',
            description=f'{message.author.name}, tu puja no es mayor a la ultima puja o a la base.',
            colour=discord.Color.red()
        )
        return embed, True
    except:
        embed = discord.Embed(
            title='ERROR',
            description=f'{message.author.name} no se pudo realizar la puja',
            colour=discord.Color.red()
        )
        embed.add_field(name='¿Que hacer?', value='Revisa el comando y el canal de ayuda o pide ayuda a un mod', inline=False)
        return embed, True
