# Copyright 2021 iiPython

# Modules
import dtp
import socket
import psutil
from src.console import console
from .exceptions import SocketError

# Client object
class Client(object):
    def __init__(self, sock: socket.socket, addr: tuple):
        self.sock = sock
        self.addr = addr

        self.log("[green]connected.")

    def __repr__(self):
        return f"{self.addr[0]}:{self.addr[1]}"

    def log(self, text):
        return console.log(f"[yellow]([cyan]{repr(self)}[yellow]): {text}")

    def send(self, data: bytes):
        self.sock.sendall(data)

    def receive(self, max_bytes: int):

        # Receive data
        data = b""
        read = 0
        while dtp.valid(data) is False:

            # Check system RAM
            if (psutil.virtual_memory().available - 2048) < (2 * (1024 ** 3)):
                console.log(f"[red]disconnected {repr(self)} due to insufficient system memory")
                raise SocketError

            recv = self.sock.recv(2048)

            # Check for completion
            if not recv:
                break

            # Save to data
            read += len(recv)
            data += recv

            # Check if data is too large
            self.log(f"[cyan]received: {read}b/{max_bytes}b max")
            if read >= max_bytes:
                self.log(f"[red]disconnected for sending over {max_bytes} bytes")
                raise SocketError

        # Check if data is empty
        if not data:
            return None

        # Return data
        return dtp.valid(data)
