import asyncio

class BotManager:
  def __init__(self, workingChannel): 
    pass

  # ? to add a discord command listener
  def use(self, name, command):
    @self.bot.command(name=name)
    async def commandMiddleware (ctx, *args):
      arguments = args if len(args) > 0 else ()
      print(arguments)
      await  command(self, ctx, *arguments)

    return self