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
            rematador = message.author.name
            remate_nombre = datos[1][7:].replace('\n','')
            remate_descripcion = datos[2][12:].replace('\n','')
            try:
                base = int(datos[3][5:].replace('\n',''))
            except:
                embed = discord.Embed(
                    title='ERROR EN BASE',
                    description='Tiene que ser un numero entero sin letras',
                    colour=discord.Color.orange()
                )
                embed.add_field(name='Ejemplo de precio base en <:nieripeso:852661603321249824>:', value='1000')
                return embed, 1

            if len(datos[4]) > 6 and datos[4][8] == '/' and datos[4][11] == '/' and datos[4][14] == ' ' and datos[4][8] == ':':
                final = str(datos[4][6:])

            else:
                embed = discord.Embed(
                    title='ERROR EN FECHA',
                    description='Es obligatorio escribir la fecha y hora de finalización de la manera que se especifica a continuación',
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
                'message_id': 0,
                'rematador': rematador,
                'nombre_rem': remate_nombre.replace('\n', ''),
                'descripcion_rem': remate_descripcion.replace('\n', ''),
                'base': base,
                'comienzo': datetime.now().strftime('%d/%m/%y %H:%M'),
                'activo': True,
                'cierre': final.replace('\n', ''),
                'postores': [],
                'foto': img
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
                title='ERROR EN ID',
                description=f'{message.author.name}, el id debe ser un número entero, nada de letras o decimales.',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        cantidad = int(datos[2][2:].strip())
        puja = [datetime.now().strftime('%d/%m/%y %H:%M'), message.author.name, cantidad, message.author.id]

        try:
            temp = db.obtener_datos(id=id_rem_apostar)
        except:
            embed = discord.Embed(
                title='ERROR DE ID',
                description=f'{message.author.name}, no existe remate con ese id.',
                colour=discord.Color.red()
            )
            return embed, True, None, None

        postores = temp["postores"]

        if temp['activo'] == False:
            print('remate terminado')
            embed = discord.Embed(
                title='ERROR DE TIEMPO',
                description=f'{message.author.name}, esta puja ya ha terminado.',
                colour=discord.Color.orange()
            )
            embed.add_field(name='GANADOR/A:', value=f'{postores[-1][1]}', inline=True)
            embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{postores[-1][2]}', inline=True)
            return embed, True, 1, None

        elif temp["rematador"] == message.author.name:
            embed = discord.Embed(
                title='ERROR EN PUJA',
                description=f'{message.author.name}, no puedes pujar en tu propio remate.',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        if postores == [] and cantidad >= temp['base'] or postores[-1][2] < cantidad:

            saved = db.guardar_puja(id=id_rem_apostar, puja=puja)

            if saved:
                temp = db.obtener_datos(id=id_rem_apostar)
                edit = discord.Embed(
                    title=f'{temp["nombre_rem"]}',
                    description=f'{temp["descripcion_rem"]}',
                    colour=discord.Color.green()
                )
                edit.add_field(name='ID del remate:', value=f'{temp["ID"]}', inline=False)
                edit.add_field(name='Rematador:', value=f'{temp["rematador"]}', inline=False)
                edit.add_field(name='Precio base:', value=f'{temp["base"]}', inline=False)
                edit.add_field(name='Fecha de finalización:', value=f'{temp["cierre"]}', inline=False)
                if temp["foto"] != None:
                    edit.set_image(url=temp["foto"])
                else:
                    edit.add_field(name='Imagen:', value='NO HAY IMAGEN DEL REMATE', inline=False)

                emb_postores = temp["postores"]
                text = ''
                for i in emb_postores:
                    text += f'{i[0]}\t' + '-\t' + f'<@{i[3]}>\t' + '-\t' + f'<:nieripeso:852661603321249824>{str(i[2])}' + '\n'
                edit.add_field(name='Postores:', value=text, inline=False)

                embed = discord.Embed(
                    title=f'**{message.author.name} realizó una puja por <:nieripeso:852661603321249824> {cantidad}.**',
                    description=f'Este remate fue abierto por **{temp["rematador"]}**',
                    colour=discord.Color.green()
                )
                return embed, False, edit, temp["message_id"]

            else:
                embed = discord.Embed(
                    title='ERROR DE TIEMPO',
                    description=f'{message.author.name}, esta puja ya ha terminado.',
                    colour=discord.Color.orange()
                )
                embed.add_field(name='GANADOR/A:', value=f'{postores[-1][1]}', inline=False)
                embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{postores[-1][2]}', inline=False)
                return embed, True, None, None

        else:
            embed = discord.Embed(
                title='ERROR EN CANTIDAD DE <:nieripeso:852661603321249824>',
                description=f'{message.author.name}, tu puja no es mayor a la ultima puja o a la base.',
                colour=discord.Color.red()
            )
            return embed, True, None, None

    except:
        embed = discord.Embed(
            title='ERROR',
            description=f'{message.author.name} no se pudo realizar la puja',
            colour=discord.Color.red()
        )
        embed.add_field(
            name='¿Que hacer?', value='Revisa el comando y el canal de ayuda o pide ayuda a un mod', inline=False)
        return embed, True, None, None