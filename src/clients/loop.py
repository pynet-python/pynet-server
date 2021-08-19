# Copyright 2021 iiPython

# Modules
import os
import dtp
import socket
import gevent
from dtp import to_bytes
from .object import Client
from src.config import config
from src.assets.states import states
from src.internals.files import FileHandler
from .exceptions import (
    DTP_MissingData, DTP_MultipleSepError, DTP_NoSepError,
    DTP_NoSuchFile, DTP_NoSuchHost, DTP_Unauthorized, SocketError
)

# Client loop
class ClientLoop(object):
    def __init__(self):
        self.threads = []
        self.max_mem = config.get("max_mem", accept = str, default = "20mb")

        # Handle max memory
        amt, den = "", ""
        for char in self.max_mem:
            try:
                amt += str(int(char))

            except ValueError:
                den += char

        amt = int(amt) * (1024 ** (["kb", "mb", "gb", "tb"].index(den) + 1))
        self.max_mem = amt

        # Load file handler
        self.file_handler = FileHandler(
            os.path.join(config.get(
                "filestore", accept = str
            ), "pages"), amt
        )

        # Miscellaneous exception messages
        self._exc_resp = {
            # DTP
            DTP_NoSepError: "DTP path has no seperator.",
            DTP_MissingData: "DTP path has missing fields.",
            DTP_MultipleSepError: "DTP path has multiple seperators.",

            # Decoding
            UnicodeDecodeError: "Invalid DTP path specified, failed to be decoded as UTF-8."
        }

    def _handle_err(self, error: Exception):
        ET = type(error)
        if ET in self._exc_resp:
            return to_bytes(
                states.MSC_ERR,
                {},
                self._exc_resp[ET].encode("UTF-8")  # Convert to bytes
            ), ET

        return None, ET

    def loop(self, client):

        # Infinite loop
        while True:

            # Receive DTP response
            try:
                data = client.receive(self.max_mem)
                if data is None:
                    break

            except SocketError:
                break  # No longer connected

            # Handle operations
            operation = None
            try:
                operation = data.headers["op"]

            except KeyError:
                response = to_bytes(
                    states.OPR_ERR,
                    {},
                    b"No operation was specified."
                )

            if operation == "get":
                try:
                    response = self.file_handler.find(data.data)
                    if isinstance(response, str):
                        response = response.encode("UTF-8")

                    decoded = data.data.decode("UTF-8")
                    filename = decoded.split(dtp.PATH_SEP)[1]

                    filename = filename.replace("\\", "/")
                    if "/" in filename:
                        filename = filename.split("/")[-1]

                    response = to_bytes(states.SUCCESS, {"filename": filename}, response)

                except Exception as Err:
                    response, ET = self._handle_err(Err)

                    # Handle no such file/host
                    if response is None:
                        if ET == DTP_NoSuchHost:
                            response = to_bytes(states.NS_HOST, {}, b"The specified host was not found on this server.")

                        elif ET == DTP_NoSuchFile:
                            response = to_bytes(states.NS_FILE, {}, b"The specified host does not have the requested file.")

                        elif ET == DTP_Unauthorized:
                            response = to_bytes(states.NT_AUTH, {}, b"You are not authorized to access this.")

                        # Handle unknown exceptions
                        else:
                            raise Err  # Unknown error

            elif operation == "list":
                try:
                    host = data.data.decode("UTF-8").strip("./\\")  # Anti-exploit (hopefully)
                    host_path = os.path.abspath(os.path.join(self.file_handler.folder, host))
                    if not os.path.isdir(host_path):
                        response = to_bytes(states.NS_HOST, {}, b"The specified host was not found on this server.")

                    response = to_bytes(
                        states.SUCCESS,
                        {},
                        "".join(line for line in (["Hostname Listing:\n"] + ["  {}\n".format(file) for file in os.listdir(host_path)])).encode("UTF-8")
                    )

                except Exception as Err:
                    response = self._handle_err(Err)

            else:
                response = to_bytes(
                    states.OPR_ERR,
                    {},
                    b"Invalid operation specified."
                )  # Invalid operation

            # Send back to client
            client.send(response)

    def handle(self, sock: socket.socket, addr: tuple):
        client = Client(sock, addr)

        # Spawn thread
        thread = gevent.spawn(self.loop, client)
        thread.start()

        self.threads.append(thread)

    def close_all(self):

        # Loop through threads
        for thread in self.threads:
            thread.kill()
