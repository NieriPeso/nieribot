from commands import est_remate_db
import discord
from . import db, edit_embed, validation

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.time import convert_to_datetime, end, get_new_close, last_30_secconds, past_date, get_date

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
                final = str(datos[4][6:]).replace('\n', '')
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
            except Exception as Err:
                embed = discord.Embed(
                    title='ERROR CON FOTO',
                    description='Es obligatorio al crear un remate subir una foto junto al mensaje',
                    colour=discord.Color.orange()
                )
                print("Error in attachment:/n/n",Err)
                return embed, 1, None

            # CONVERTIR PRECIO A NUMERO ENTERO
            try:
                base = int(base)
            except ValueError as Err:
                base = 0
                print("Error converting price to integer:/n/n",Err)

            # PERSISTENCIA EN MONGO DB
            save = est_remate_db.estructura(
                id_remate,
                rematador,
                message.author.id,
                remate_nombre,
                remate_descripcion,
                base,
                get_date(),
                convert_to_datetime(final),
                img
            )

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

    except Exception as Err:
        embed = discord.Embed(
            title='ERROR CREANDO REMATE',
            description=f'Lo siento <@{message.author.id}> pero tu remate no pudo registrarse, algo esta mal.\nComprueba como escribiste el comando y corrígelo o pidele ayuda a un mod.',
            colour=discord.Color.red()
        )
        print("Error creating budget:/n/n",Err)
        return embed, 1, None

def pujar_remate(message):
    try:
        puja = message.content.lower()
        datos = puja.split('*')
        if not datos[1].startswith('id ') or not datos[2].startswith('ñ '):
            embed = discord.Embed(
                title='ERROR EN COMANDO',
                description=f'{message.author.name}, introdujiste mal el comando de puja.',
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

        postores = temp["offers"]

        if end(temp['closeAt']) or not temp['active']:
            embed = discord.Embed(
                    title='ERROR DE TIEMPO',
                    description=f'<@{message.author.id}>, este remate ya ha terminado.',
                    colour=discord.Color.orange()
                )
            try:
                embed.add_field(name='GANADOR/A:', value=f'<@{postores[-1][3]}> :hammer: :tada: <:nieripeso:852661603321249824>', inline=False)
                embed.add_field(name='Cantidad pujada:', value=f'<:nieripeso:852661603321249824>{postores[-1][2]}', inline=False)
            except Exception as Err:
                embed.add_field(name='GANADOR/A:', value='Parece que **nadie** pujó en este remate', inline=False)
                embed.add_field(name='Nota:', value=f'Lo siento <@{temp["ownerId"]}>,\nParece que nadie pujó a tu\nremate de: **{temp["name"]}**', inline=False)
                print("Error with list of offers:/n/n",Err)
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

        puja = {
            'createdAt': get_date(),
            'bidderName': message.author.name,
            'amount': cantidad,
            'bidderId': message.author.id
        }

        if temp["ownerName"] == message.author.name:
            embed = discord.Embed(
                title='ERROR EN PUJA',
                description=f'{message.author.name}, no puedes pujar en tu propio remate.',
                colour=discord.Color.orange()
            )
            return embed, True, None, None

        if postores == [] and cantidad >= temp['baseAmount'] or postores[-1]['amount'] < cantidad:
            if postores == [] and cantidad == 0:
                embed = discord.Embed(
                    title='ERROR EN CANTIDAD DE <:nieripeso:852661603321249824>',
                    description=f'{message.author.name}, la **cantidad minima** para pujar es de: <:nieripeso:852661603321249824> **1**.',
                    colour=discord.Color.orange()
                )
                return embed, True, None, None
            db.guardar_puja(id=id_rem_apostar, puja=puja)
            temp = db.obtener_datos(id=id_rem_apostar)
            postores = temp["offers"]

            embed = discord.Embed(
                title=f'{message.author.name} realizó una puja por <:nieripeso:852661603321249824> {cantidad}.',
                description=f'Este remate fue abierto por <@{temp["ownerId"]}>',
                colour=discord.Color.green()
            )
            embed.add_field(name='Pujaste a:', value=f'{temp["name"]}', inline=False)
            embed.add_field(name='Post de remate', value=f'[Remate en cartelera](https://discord.com/channels/847456853465497601/854807245509492808/{temp["messageId"]})', inline=False)

            if last_30_secconds(puja['createdAt'], temp['closeAt']):
                new_close = get_new_close(puja['createdAt'], temp['closeAt'])
                temp['closeAt'] = new_close.strftime('%d/%m/%Y %H:%M')
                embed.add_field(name='AVISO DE ULTIMOS 30 SEGUNDOS', value='Esta puja se realizó en los ultimos 30 segundos, este remate ahora cierra dentro de un minuto', inline=False)
                embed.add_field(name='NUEVO CIERRE', value=f'{temp["closeAt"].strftime("%d/%m/%Y %H:%M")}')
                db.alargar_remate(temp['id'], new_close)

            edit = edit_embed.edit_embed(data=temp)

            return embed, False, edit, temp["messageId"]

        else:
            if len(postores) > 0:
                embed = discord.Embed(
                    title='ERROR EN CANTIDAD DE <:nieripeso:852661603321249824>',
                    description=f'{message.author.name}, tu puja no es mayor a la ultima puja con: <:nieripeso:852661603321249824> {postores[-1]["amount"]}.',
                    colour=discord.Color.red()
                )
                embed.add_field(name='CANTIDAD SUGERIDA PARA PUJAR', value=f'<:nieripeso:852661603321249824> {postores[-1]["amount"]+1}')
                return embed, True, None, None
            else:
                embed = discord.Embed(
                    title='ERROR EN CANTIDAD DE <:nieripeso:852661603321249824>',
                    description=f'{message.author.name}, tu puja no es mayor a la base.',
                    colour=discord.Color.red()
                )
                return embed, True, None, None

    except Exception as Err:
        embed = discord.Embed(
            title='ERROR',
            description=f'{message.author.name} no se pudo realizar la puja',
            colour=discord.Color.red()
        )
        embed.add_field(
            name='¿Que hacer?', value='Revisa el comando y el canal de ayuda o pide ayuda a un mod', inline=False)
            print("Error with the command flux of offer in a budget:/n/n",Err)
        return embed, True, None, None

def cerrar_remate(ctx, id, motive):
    if validation.validate_permissions(ctx):
        _id, ID, msg_id, rematador, id_rem, nombre_rem, desc_rem, base, postores, foto, comienzo = est_remate_db.extraer_datos(db.obtener_datos(id))
        doc = est_remate_db.estructura(
            id_remate=ID,
            rematador=rematador,
            id_rem=id_rem,
            remate_nombre=nombre_rem,
            remate_descripcion=desc_rem,
            base=base,
            comienzo=comienzo,
            final=get_date(),
            img=foto,
            deletedAt=get_date(),
            message_id=msg_id,
            postores=postores
            )
        db.close_remate(id, doc, _id)
        data = db.obtener_datos(id)
        embed = discord.Embed(
            tittle='REMATE BORRADO',
            discord=f'<@{ctx.message.author.id}> ha borrado el remate.',
            color=discord.Color.green()
        )
        embed.add_field(name='Id del remate:', value=f'{data["id"]}', inline=False)
        embed.add_field(name='Rematador:', value=f'<@{data["ownerId"]}>', inline=False)
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
