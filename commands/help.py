import discord

async def help_command(bot_manager, ctx, *args):
    user = ctx.message.author.id
    if not args:
        embed = discord.Embed(
            title='LO SIENTO',
            description=f'<@{user}> este comando está en construccion por el momento',
            colour=discord.Color.dark_orange()
        )
    await ctx.send(embed=embed)

