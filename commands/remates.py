import discord
from . import db
from datetime import datetime

def crear_remate(message):
    try:
        remate = message.content.lower()

        if len(remate) < 15:
            return None, None

        datos = remate.split('*')

        if not datos[1].startswith('nombre ') and not datos[2].startswith('descripcion ') and not datos[3].startswith('base ') and not datos[4].startswith('final '):
            embed = discord.Embed(
                title='ERROR EN COMANDO',
                description='Los nombres para los campos son **obligatorios**.',
                colour=discord.Color.orange()
            )
            embed.set_footer(text='EJEMPLO:')
            return embed, 2
        
        else:
            id_remate = db.cantidad_remates()
            rematador = str(message.author.name)
            remate_nombre = str(datos[1][7:])
            remate_descripcion = str(datos[2][12:])
            base = datos[3][5:]

            if len(datos[4]) > 6:
                final = str(datos[4][6:])

            else:
                embed = discord.Embed(
                    title='ERROR',
                    description='Es obligatorio escribir la fecha y hora de finalización',
                    colour=discord.Color.orange()
                )
                embed.add_field(name='Formato de ejemplo de fecha:', value='20/04/22 16:20')
                return embed, 1

            try:
                img = message.attachments[0].url
            except:
                img = None

            # CONVERTIR PRECIO A NUMERO ENTERO
            try:
                base = int(base)
            except ValueError:
                base = 0

            # PERSISTENCIA EN MONGO DB
            save = {
                'ID': id_remate,
                'Rematador': rematador,
                'Nombre de remate': remate_nombre.replace('\n', ''),
                'Descripcion del remate': remate_descripcion.replace('\n', ''),
                'Base': base,
                'Comienzo': datetime.now().strftime('%d/%m/%y %H:%M'),
                'Activo': True,
                'Termina': final.replace('\n', ''),
                'Postores': [],
                'Foto':img
            }

            db.agregar_remate(save)

            embed = discord.Embed(
                title=f'{remate_nombre}',
                description=f'{remate_descripcion}',
                colour=discord.Color.green()
            )
            embed.add_field(name='ID del remate:', value=f'{id_remate}', inline=False)
            embed.add_field(name='Rematador:', value=f'{rematador}', inline=False)
            embed.add_field(name='Precio base:', value=f'{base}', inline=False)
            embed.add_field(name='Fecha de finalización:', value=f'{final}', inline=False)
            if not img == None:
                embed.set_image(url=img)
            else:
                embed.add_field(
                    name='Imagen:', value='NO HAY IMAGEN DEL REMATE', inline=False)
                embed.set_footer(text='SUERTE A TODOS')
            return embed, 0

    except:
        embed = discord.Embed(
            title='ERROR CREANDO REMATE',
            description=f'Lo siento {message.author.name} pero tu remate no pudo registrarse, algo esta mal.\nComprueba como escribiste el comando y corrígelo o pidele ayuda a un mod.',
            colour=discord.Color.red()
        )
        return embed, 1


def pujar_remate(message):
    try:
        puja = message.content.lower()
        datos = puja.split('*')

        try:
            id_rem_apostar = int(datos[1][3:].replace('\n', ''))

        except:
            embed = discord.Embed(
                title='ERROR',
                description=f'{message.author.name}, el id debe ser un número entero, nada de letras o decimales.',
                colour=discord.Color.orange()
            )
            return embed, True
        
        cantidad = int(datos[2][2:].replace('\n', ''))
        puja = [message.author.name, cantidad]

        temp = db.obtener_datos(id=id_rem_apostar)
        postores = temp['Postores']

        if temp["Rematador"] == message.author.name:
            embed = discord.Embed(
                title='ERROR',
                description=f'{message.author.name}, no puedes pujar en tu propio remate.',
                colour=discord.Color.orange()
            )
            return embed, True

        if postores == [] and cantidad >= temp['Base'] or postores[-1][1] < cantidad:

            saved = db.guardar_puja(id=id_rem_apostar, puja=puja)

            if saved:
                embed = discord.Embed(
                    title=f'**{message.author.name} realizó una puja por <:nieripeso:852661603321249824> {cantidad}.**',
                    description=f'Este remate fue abierto por **{temp["Rematador"]}**',
                    colour=discord.Color.green()
                )                
                return embed, False

            else:
                embed = discord.Embed(
                    title='ERROR',
                    description=f'{message.author.name}, esta puja ya ha terminado.',
                    colour=discord.Color.red()
                )
                embed.add_field(name='GANADOR/A:', value=f'{postores[-1][0]}', inline=False)
                embed.add_field(name='Cantidad pujada:', value=f'{postores[-1][1]}', inline=False)
                return embed, True

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
        embed.add_field(
            name='¿Que hacer?', value='Revisa el comando y el canal de ayuda o pide ayuda a un mod', inline=False)
        return embed, True