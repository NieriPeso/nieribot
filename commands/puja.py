from utils import remates
from commands import chat

# COMANDO PARA PUJAR EN LOS REMATES
async def pujar(bot_manager, ctx, *args):
  bot = bot_manager.bot
  if ctx.message.channel.id == 849410645513207828:
    if args:
        embed, error, edit, id_msg = remates.pujar_remate(message=ctx.message)
        if not error:
            channel = bot.get_channel(854807245509492808)
            msg = await channel.fetch_message(id_msg)
            await chat.editar_msg_remate(message=msg, embed=edit)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed)
            if edit:
                await ctx.send('$puja\n*id 1\n*Ñ 1000')
    else:
        await ctx.send('$puja\n*id \n*Ñ ')
