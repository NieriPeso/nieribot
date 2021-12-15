from sockets.bootstrap import Socket

# ? Importing socket modules
from sockets.modules.sales import Sales as SalesModule 

# ? defining the sockets server instance to be used by the bot sending the modules we'll use
SocketManager = Socket(['/sales'])


SocketManager.modules([
  SalesModule
])
