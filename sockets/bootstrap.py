from decouple import config
import socketio

# * Socket master bootstrap
class Socket:
  # ? socket server connection configurations
  socket_server_url = config('SOCKETS_SERVER_URL')
  socket_namespaces = []
  socket_server_key = config('SOCKETS_SERVER_KEY')

  ####################### ? #######################
  sio = socketio.AsyncClient() # ? socket client instance
  socket_modules = {} # ? sockets modules are saved in this dictionary after run them.

  def __init__ (self, namespaces): 
    self.socket_namespaces = namespaces

  # * Connecting to the socket server at the first time.
  async def run (self): 
    await self.sio.connect(self.socket_server_url, namespaces=self.socket_namespaces, auth=self.auth())
    await self.sio.wait()

  # * Initializing every socket modules.
  def modules(self, mds): 
    print('LOADING SOCKET MODULES')
    for Module in mds: 
      module_name = Module.__name__
      module_object = Module(self.sio)
      self.socket_modules[module_name] = module_object
      
  # * get module by name
  def module(self, module_name): 
    module_exists = module_name in self.socket_modules
    if(module_exists):
      print(self.socket_modules, self.socket_modules[module_name])
      return self.socket_modules[module_name]
    else: 
      return None

  # * Getting authentication payload to send to the socket server.
  def auth(self):
    return {'socketKey': self.socket_server_key}
