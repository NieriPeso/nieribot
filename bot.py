import discord
from discord.ext import commands
from decouple import config

client = commands.Bot(command_prefix = '$')

# INICIO DEL BOT PARA SU FUNCIONAMIENTO
@client.event
async def on_ready():
    print(f'Nieribot listo y operando con el user: {client.user}')


@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if channel.id == 850823068472836097:
        print(f'Reaccion con {reaction.emoji}')


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


    # CASA DE SUBASTAS, REGISTRO DE LA MISMA
    if message.content.startswith('$subasta'):
        msg = message.content
        print('\n\nSubasta:\n')
        print(msg.split("-"))


    # BORRADO DE 50 MENSAJES EN UN CANAL (HAY QUE HACER EL FILTRO PARA LOS MODERADORES USAR SOLAMENTE)
    if message.content.startswith('$clear-chat'):
        listamsg = message.content.split(" ")
        if len(listamsg) > 1:
            await message.channel.purge(limit=int(listamsg[1]))
            print('Borrado el chat con el parametro:',int(listamsg[1]))
        else:
            await message.channel.purge(limit=50)
            print('Borrado el chat sin parametros')


    # ESCUCHAR EL COMANDO '$nieripeso' EN CUALQUIER CANAL PARA ENVIAR INSTRUCCIONES POR PRIV.
    if message.content.startswith('$nieripeso'):
        await message.author.send('''
Primero que nada necesitas descargar la aplicación Metamask (https://metamask.io/download). 
Una vez descargada la aplicación debes crear una nueva Wallet. 
(Si ya tenes una no es necesario hacer otra cuenta).
ATENCIÓN: Es de suma importancia anotar en un papel las palabras que aparecen al momento que creamos una nueva wallet en Metamask. Es la única manera de poder recuperar una cuenta en caso de perderla. Recomendamos que guarde dicho papel en algún lugar de suma seguridad como respaldo de seguridad.
    ''')
        await message.author.send('''
Ya creada la Wallet, procede a pasarte a la red BSC Mainnet, es la red sobre la que opera el Ñieri. 
Para eso debes abrir las configuraciones de red de dentro la aplicación. 
Menu > Settings > Networks > Add Network
Luego procede a llenar los casilleros con la siguiente información:
TIP: se puede hacer copy-paste.
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
¡¡Ya puedes recibir tus Ñieri, Ñieri!!
        ''')
        await message.author.send('''
Por último, para recibir tus Ñieri debes compartir el código haciendo click en la moneda.
Entramos en Receive; Nos muestra un código QR y un link (0x...). 
Comparte este código en Discord para recibir Ñieri.

IMPORTANTE: Para poder transferir Ñieri a otras personas debes pagar una pequeña cuota por la transacción, para eso debes tener un poco de BNB, la cryptomoneda de Binance. Aparece por defecto cuando nos conectamos a la red BSC Mainnet. Puedes pedir tus BNB en #quierobnb.
        ''')


# EJECUCIÓN DEL BOT -SE SUPONE QUE ESE TOKEN ES SECRETO!-
client.run(config('TOKEN'))