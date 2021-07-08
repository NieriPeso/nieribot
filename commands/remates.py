import discord, pytz
from . import db, edit_embed, validation

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.time import end, past_date, get_date

tz = pytz.timezone('America/Argentina/Buenos_Aires')

def crear_remate(message):
    try:
        remate = message.content.lower()

        if len(remate) < 15:
            return None, None, None

        datos = remate.split('*')

        if not datos[1].startswith('nombre ') or not (datos[2].startswith('descripcion ') or datos[2].startswith('descripción ')) or not datos[3].startswith('base ') or not datos[4].startswith('final '):
            embed = discord.Embed(
                title='ERROR EN COMANDO',
                description='Los nombres para los campos son **obligatorios**.',
                colour=discord.Color.orange()
            )
            embed.set_footer(text='EJEMPLO:')
            return embed, 2, None

        else:
            id_remate = db.cantidad_remates()
            rematador = message.author.name
            remate_nombre = datos[1][7:].replace('\n','')
            remate_descripcion = datos[2][12:]
            try:
                base = int(datos[3][5:].replace('\n',''))
            except:
                embed = discord.Embed(
                    title='ERROR EN BASE',
                    description='Tiene que ser un numero entero sin letras',
                    colour=discord.Color.orange()
                )
                embed.add_field(name='Ejemplo de precio base en <:nieripeso:852661603321249824>:', value='1000')
                return embed, 1, None

            if len(datos[4]) > 6 and datos[4][8] == '/' and datos[4][11] == '/' and datos[4][16] == ' ' and datos[4][19] == ':':
                final = str(datos[4][6:])
                if past_date(final):
                    embed = discord.Embed(
                        title='ERROR EN FECHA',
                        description='Es obligatorio escribir una fecha y hora de finalización futura, no puede haber pasado ya o tener un rango de tiempo de remate menor a 10 minutos.',
                        colour=discord.Color.orange()
                    )
                    embed.add_field(name='Fecha y hora en este momento:', value=get_date().strftime('%d/%m/%y %H:%M'))
                    return embed, 1, None

            else:
                embed = discord.Embed(
                    title='ERROR EN FECHA',
                    description='Es obligatorio escribir la fecha y hora de finalización de la manera que se especifica a continuación',
                    colour=discord.Color.orange()
                )
                embed.add_field(name='Formato de ejemplo de fecha:', value='20/04/2022 16:20')
                return embed, 1, None

            try:
                img = message.attachments[0].url
            except:
                img = 'https://cdn.discordapp.com/attachments/860489778646876170/860972003922149396/image0.png'

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
                'id_rematador': message.author.id,
                'nombre_rem': remate_nombre,
                'descripcion_rem': remate_descripcion,
                'base': base,
                'comienzo': get_date().strftime('%d/%m/%y %H:%M'),
                'activo': True,
                'cierre': final.replace('\n', ''),
                'postores': [],
                'foto': img,
                'deletedAt': None
            }

            db.agregar_remate(save)

            confirm = discord.Embed(
                title='Se ha creado un remate',
                description=f'Titulo: {remate_nombre}\nID: {id_remate}\nBase: <:nieripeso:852661603321249824>{base}',
                colour=discord.Color.green()
            )

            embed = discord.Embed(
                title=f'{remate_nombre}',
                description=f'{remate_descripcion}',
                colour=discord.Color.green()
            )
            embed.add_field(name='ID del remate:', value=f'{id_remate}', inline=False)
            embed.add_field(name='Rematador:', value=f'<@{message.author.id}>', inline=False)
            embed.add_field(name='Precio base:', value=f'{base}', inline=False)
            embed.add_field(name='Fecha de finalización:', value=f'{final}', inline=False)
            # if not img == None:
            embed.set_image(url=img)
            # else:
            #     embed.add_field(
            #         name='Imagen:', value='NO HAY IMAGEN DEL REMATE', inline=False)
            return embed, 0, confirm

    except:
        embed = discord.Embed(
            title='ERROR CREANDO REMATE',
            description=f'Lo siento <@{message.author.id}> pero tu remate no pudo registrarse, algo esta mal.\nComprueba como escribiste el comando y corrígelo o pidele ayuda a un mod.',
            colour=discord.Color.red()
        )
        return embed, 1, None

def agregar_foto(message, id):
    data = db.obtener_datos(id)
    if data != None and data['activo'] == True and message.author.id == data['id_rematador']:
        try:
            img = message.attachments[0].url
        except:
            embed = discord.Embed(
                title='ERROR',
                description='Parece que no subiste foto',
                color=discord.Color.red()
            )
            return embed, True, None, None
        db.add_picture(id, img=img)
        embed = discord.Embed(
            title='FOTO AGREGADA',
            description=f'<@{message.author.id}>, tu foto se ha agregado correctamente.',
            color=discord.Color.green()
        )
        data=db.obtener_datos(id)
        edit = edit_embed.edit_embed(data = data)
        return embed, False, edit, data['message_id']
    else:
        embed = discord.Embed(
            title='ERROR',
            description=f'Parece que el remate con id {id} no existe, ya cerró o no es de tu propiedad <@{message.author.id}>',
            color=discord.Color.red()
        )
        return embed, True, None, None

def pujar_remate(message):
    try:
        puja = message.content.lower()
        datos = puja.split('*')
        if not datos[1].startswith('id ') or not datos[2].startswith('ñ '):
            embed = discord.Embed(
                title='ERROR EN COMANDO',
                description=f'{message.author.name}, introduciste mal el comando de puja.',
                colour=discord.Color.orange()
            )
            embed.set_footer(text='EJEMPLO:')
            return embed, True, True, None
        if datos[1][3:].replace('\n','').strip().isnumeric():
            id_rem_apostar = int(datos[1][3:].replace('\n', '').strip())
        else:
            embed = discord.Embed(
                title='ERROR EN ID',
                description=f'{message.author.name}, el id debe ser un número entero, nada de letras o decimales.',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        temp = db.obtener_datos(id=id_rem_apostar)

        if temp == None:
            embed = discord.Embed(
                title='ERROR DE ID',
                description=f'{message.author.name}, no existe remate con ese id.',
                colour=discord.Color.red()
            )
            return embed, True, None, None

        postores = temp["postores"]

        if end(temp['cierre']):
            db.terminar_remate(id=id_rem_apostar)
            embed = discord.Embed(
                    title='ERROR DE TIEMPO',
                    description=f'<@{message.author.id}>, esta puja ya ha terminado.',
                    colour=discord.Color.orange()
                )
            try:
                embed.add_field(name='GANADOR/A:', value=f'<@{postores[-1][3]}> :hammer: :tada: <:nieripeso:852661603321249824>', inline=False)
                embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{postores[-1][2]}', inline=False)
            except:
                embed.add_field(name='GANADOR/A:', value='Parece que **nadie** pujó en este remate', inline=False)
                embed.add_field(name='Nota:', value=f'Lo siento <@{temp["id_rematador"]}>,\nParece que nadie pujó a tu\nremate de: **{temp["nombre_rem"]}**', inline=False)
            return embed, True, None, None
        elif datos[2][2:].isnumeric():
            cantidad = int(datos[2][2:].strip())
        else:
            embed = discord.Embed(
                title='ERROR EN CANTIDAD DE <:nieripeso:852661603321249824>',
                description=f'{message.author.name}, la cantidad de <:nieripeso:852661603321249824> con la que decides entrar **no es un numero entero.**',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        puja = [get_date().strftime('%d/%m/%y %H:%M'), message.author.name, cantidad, message.author.id]

        if temp["rematador"] == message.author.name:
            embed = discord.Embed(
                title='ERROR EN PUJA',
                description=f'{message.author.name}, no puedes pujar en tu propio remate.',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        if postores == [] and cantidad >= temp['base'] or postores[-1][2] < cantidad:
            db.guardar_puja(id=id_rem_apostar, puja=puja)
            temp = db.obtener_datos(id=id_rem_apostar)
            postores = temp["postores"]

            edit = edit_embed.edit_embed(data=temp)

            embed = discord.Embed(
                title=f'{message.author.name} realizó una puja por <:nieripeso:852661603321249824> {cantidad}.',
                description=f'Este remate fue abierto por <@{temp["id_rematador"]}>',
                colour=discord.Color.green()
            )
            embed.add_field(name='Pujaste a:', value=f'{temp["nombre_rem"]}', inline=False)
            embed.add_field(name='Post de remate', value=f'[Remate en cartelera](https://discord.com/channels/847456853465497601/854807245509492808/{temp["message_id"]})', inline=False)
            return embed, False, edit, temp["message_id"]

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

def borrar_remate(ctx, id, motive):
    if validation.validate_permissions(ctx):
        db.close_remate(id)
        data = db.obtener_datos(id)
        embed = discord.Embed(
            tittle='REMATE BORRADO',
            discord=f'<@{ctx.message.author.id}> ha borrado el remate.',
            color=discord.Color.green()
        )
        embed.add_field(name='Id del remate:', value=f'{data["ID"]}', inline=False)
        embed.add_field(name='Rematador:', value=f'{data["rematador"]}', inline=False)
        if motive != None:
            embed.add_field(name='Motivo de cierre:', value=f'{motive}', inline=False)
        else:
            embed.add_field(name='Motivo de cierre:', value='No hubo especificación del motivo.', inline=False)
        return embed
    else:
        embed = discord.Embed(
            tittle='ERROR DE PERMISOS',
            description=f'<@{ctx.message.author.id}>, parece que no tienes permisos para cerrar remates.',
            color=discord.Color.red()
        )
        return embed