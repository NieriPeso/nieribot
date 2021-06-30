import discord
from . import db

enable = False

def registro(wallet, name):
  if enable:
    return db.nuevo_nieri(name=name, wallet=wallet)

  embed = discord.Embed(
    title=f'LO SIENTO {name}',
    description=f'Esta feature esta desactivada',
    colour=discord.Color.orange()
  )
  return embed

# COMANDO PARA REGISTRAR NUEVOSNIERIS Y SUS WALLETS PARA LA ENTREGA DE $Ñ
async def registro_nieri_command(bot_manager, ctx, *args):
  wallet = args[0] if len(args) > 0 else 'wallet'
  embed = registro(wallet=wallet, name=ctx.message.author.name)
  await ctx.send(embed=embed)