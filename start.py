# DTP
# Copyright 2021 iiPython (Benjamin O'Brien)

# Gevent initialization
import gevent
from gevent import monkey

monkey.patch_all()
gevent.get_hub().NOT_ERROR += (KeyboardInterrupt,)

# Modules
from src import Server

# Initialization
server = Server()

# Start server
server.run()
