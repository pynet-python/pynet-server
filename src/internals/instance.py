# Copyright 2021 iiPython

# Modules
import sys
import socket
from src.config import config
from src.console import console
from src.clients import ClientLoop

# Server class
class Server(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(family = socket.AF_INET, type = socket.SOCK_STREAM)

        # Handle connection
        self.port = config.get("port", accept = int, min = 1)
        self.loop = ClientLoop()

        try:
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.bind(("0.0.0.0", self.port))

        except OSError:
            return console.exit(1, f"[red]Failed to bind to 0.0.0.0:{self.port}")

    def _shutdown(self):
        print("\r", end = "")  # Stop ^C text
        console.log("[red]Shutting down server...")

        # Kill client threads
        self.loop.close_all()

        # Shutdown socket
        self.shutdown(0)
        self.close()

        # Close script
        console.log("[green]Goodbye.")
        return sys.exit(0)

    def run(self):
        """
        Starts the DTP server
        """

        # Handle logging
        console.log(f"[green]Listening on 0.0.0.0:{self.port}")

        # Handle clients
        self.listen(config.get("most_no_thread", accept = int, min = 1, default = 5))
        while True:
            try:
                sock, addr = self.accept()
                self.loop.handle(sock, addr)

            except KeyboardInterrupt:

                # Shutdown server
                return self._shutdown()
