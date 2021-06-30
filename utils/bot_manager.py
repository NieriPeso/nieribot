import asyncio

class BotManager:
  def __init__(self, working_channel): 
    self.working_channel = working_channel

  # ? To add a discord command listener
  def use(self, name, command):
    @self.bot.command(name=name)
    async def commandMiddleware (ctx, *args):
      if args:
        await command(self, ctx, *args)
      else: 
        await command(self, ctx)
    return self