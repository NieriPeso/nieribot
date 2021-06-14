import discord
from discord.ext import commands
from decouple import config
import json
from datetime import datetime

# ESTRUCTURA DE COMANDOS Y ACCIONES DEL BOT

client = commands.Bot(command_prefix = '/')

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
@client.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {client.user}')


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 852333212373745674:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'acepto':
            role = discord.utils.get(guild.roles, name='nieris')
            #print(f'Role: {role}')
        else:
            role = None
            #print('Otro emoji agregado')

        if role is not None:
            member = payload.member
            if member is not None:
                await payload.member.add_roles(role)
                #print('Rol agregado, nuevo nieri')


@client.event
async def on_message(message):
    if message.author == client.user:
        return



    # BORRADO DE 50 MENSAJES EN UN CANAL (HAY QUE HACER EL FILTRO PARA LOS MODERADORES USAR SOLAMENTE)
    if message.content.startswith('$clear-chat'):
        listamsg = message.content.split(" ")
        if len(listamsg) > 1:
            await message.channel.purge(limit=int(listamsg[1]))
            print('Borrado el chat con el parametro:',int(listamsg[1]))
        else:
            await message.channel.purge(limit=50)
            print('Borrado el chat sin parametros')


    if message.content.startswith('$nuevonieri'):
        sep = message.content.split(' ')
        if len(sep) > 1:
            f = open('nuevosnieris.json','r')
            temp = json.load(f)
            f.close()
            temp[message.user.id] = {
                "Wallet": sep[1],
                "Entregado":False
            }
            f = open('nuevosnieris.json','w')
            json.dump(temp, f, indent=2)
            f.close()


    #============================== REMATE-VALORATE ==============================
    
    # COMANDO PARA PLANTARSE A UN REMATE
    if message.content.startswith('$puja'):
        print('\nApostando en remate\n')
        apuesta = message.content
        datos = apuesta.split('*')

        id_rem_apostar = str(datos[1][2:]).replace('\n','')
        cantidad = int(datos[2][9:].replace('\n',''))
        apuesta = [message.author.name, cantidad]
        
        file = open('remates.json', 'r')
        temp = json.load(file)
        file.close()
        
        postores = temp[id_rem_apostar]['Postores']
        postores.append(apuesta)
        
        temp[id_rem_apostar]['Postores'] = postores

        channel = client.get_channel(852910494876172309)

        await channel.send(f'''
El usuario de nombre **{message.author.name}**
Levanta la puja con **$Ñ {cantidad}**
Al remate con id **{id_rem_apostar}** de **{temp[id_rem_apostar]['Rematador']}**

**HAGAN SUS APUESTASS CON EL SIGUIENTE COMANDO *(copy-paste recomendado)***
\n
        ''')
        await channel.send(f'''
$puja
*id su_id
*cantidad numero_base_$Ñ
        ''')

        file = open('remates.json', 'w')
        json.dump(temp, file, indent=2)
        file.close()



    # COMANDO PARA EL REGISTRO DE LOS REMATES
    if message.content.startswith('$crear-remate'):
        print('\nRegistro de remate\n')
        remate = message.content
        datos = remate.split('*')

        id_remate = str(datos[1][2:])
        rematador = str(message.author.name)
        remate_nombre = str(datos[2][7:])
        remate_descripcion = str(datos[3][12:])
        base = datos[4][5:]
        final = str(datos[5][6:])

        # CONVERTIR PRECIO A NUMERO ENTERO
        try:
            base = int(base)
        except ValueError:
            print('Precio inicial no es un int. ValueError')


        # ESCRIBIR A ARCHIVO CON REMATES
        file = open('remates.json', 'r')
        temp = json.load(file)
        file.close()
        temp[id_remate.replace('\n','')] = {
            'Rematador': rematador,
            'Nombre de remate': remate_nombre.replace('\n',''),
            'Descripcion del remate': remate_descripcion.replace('\n',''),
            'Base': base,
            'Comienzo':datetime.now().strftime('%d/%m/%y %H:%M'),
            'Activo':True,
            'Termina': final.replace('\n',''),
            'Postores':[]
        }
        file = open('remates.json', 'w')
        json.dump(temp, file, indent=2)
        file.close()


        channel = client.get_channel(852910494876172309)

        await channel.send(f'''
ID del remate: ***{id_remate}***
Rematador: **{rematador}**\n
Nombre del remate: {remate_nombre}
Descripción del remate: {remate_descripcion}
Precio base: **{base}**\n
Fecha límite: **{final}**

**HAGAN SUS APUESTASS**
\n
        ''')

        #===========================================================================



    # ESCUCHAR EL COMANDO '$nieripeso' EN CUALQUIER CANAL PARA ENVIAR INSTRUCCIONES POR PRIV.
    if message.content.startswith('$nieripeso'):
        await message.author.send('**PUEDES ENTRAR EN #tutoriale PARA VER UN VIDEO**')
        await message.author.send('''
Primero que nada necesitas descargar la aplicación Metamask (https://metamask.io/download). 
Una vez descargada la aplicación debes crear una nueva Wallet. 
(Si ya tenes una no es necesario hacer otra cuenta).
**ATENCIÓN: Es de suma importancia anotar en un papel las palabras que aparecen al momento que creamos una nueva wallet en Metamask.
Es la única manera de poder recuperar una cuenta en caso de perderla. Recomendamos que guarde dicho papel en algún lugar de suma seguridad como respaldo de seguridad.**
    ''')
        await message.author.send('''
Ya creada la Wallet, procede a pasarte a la red BSC Mainnet, es la red sobre la que opera el Ñieri. 
Para eso debes abrir las configuraciones de red de dentro la aplicación. 
Menu > Settings > Networks > Add Network
Luego procede a llenar los casilleros con la siguiente información:
**TIP: *SE SUGIERE HACER COPY-PASTE.***
            ''')
        await message.author.send('NETWORK NAME:')
        await message.author.send('BSC Mainnet')
        await message.author.send('RPC URL:')
        await message.author.send('https://bsc-dataseed.binance.org/')
        await message.author.send('CHAIN ID:')
        await message.author.send('56')
        await message.author.send('SYMBOL:')
        await message.author.send('BNB')
        await message.author.send('BLOCK EXPLORER URL:')
        await message.author.send('https://bscscan.com/')
        await message.author.send('''
Una vez agregada la red BSC Mainnet necesitamos agregar la Ñieri como una nueva token.
Para eso seleccionamos + ADD TOKENS en tu Wallet.
Introducimos el siguiente código de la Ñieri en Token Adress
        ''')
        await message.author.send('0x811496d46838ccf9bba46030168cf4d7d588d04a')
        await message.author.send('''
Automáticamente la app reconoce el token y llena el resto de los casilleros.
Llenos todos los casillero aprieta en ADD TOKEN
De esta manera logramos ver la Ñieri en la wallet 
**¡¡Ya puedes recibir tus Ñieri, Ñieri!!**
        ''')
        await message.author.send('''
**Por último, para recibir tus Ñieri debes compartir el código haciendo click en la moneda.
Entramos en Receive; Nos muestra un código QR y un link (0x...). 
Comparte este código en #:moneybag:quieromisñeris.**

**IMPORTANTE: Para poder transferir Ñieri a otras personas debes pagar una pequeña cuota por la transacción, para eso debes tener un poco de BNB, la cryptomoneda de Binance.
Aparece por defecto cuando nos conectamos a la red BSC Mainnet. Puedes pedir tus BNB en #:money_with_wings:quierobnb.**
        ''')


# EJECUCIÓN DEL BOT
client.run(config('TOKEN'))