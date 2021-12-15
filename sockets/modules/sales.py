class Sales: 
  def __init__(self, sio): 
    self.sio = sio
    self.events()

  # ? define event listeners on_connect, on_disconnect, etc
  def events(self): 
    self.sio.on('connect', self.on_connect, namespace='/sales')

  # * EVENT HANDLERS
  async def on_connect(args):
    print('socket connection')

  # * Emitters 
  async def create_sale(self, data):
    formattedData = { **data, 'provider': 'discord' }
    formattedData['startAt'] = data['startAt'].isoformat()
    formattedData['closeAt'] = data['closeAt'].isoformat()
    del formattedData['_id']
    await self.sio.emit('create', formattedData,  namespace='/sales')