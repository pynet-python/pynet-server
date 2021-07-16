# Copyright 2021 iiPython

# Modules
import os
import dtp
import psutil
from src.console import console
from src.clients.exceptions import (
    DTP_MissingData, DTP_MultipleSepError, DTP_NoSepError,
    DTP_NoSuchFile, DTP_NoSuchHost, DTP_Unauthorized
)

# Handler
class FileHandler(object):
    def __init__(self, folder: str, max_mem: int):
        self.folder = folder
        self.max_mem = max_mem

        try:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

        except OSError:
            console.exit(1, "[red]Failed to create file store: '{}', please create it manually.".format(self.folder))

    def tounix(self, path):
        return path.replace("\\", "/")

    def find(self, dtp_path: bytes):
        path = dtp_path.decode("UTF-8")

        # Seperate data
        pathdata = path.split(dtp.PATH_SEP)
        if len(pathdata) > 2:
            raise DTP_MultipleSepError

        if dtp.PATH_SEP not in path:
            raise DTP_NoSepError

        # Handle path
        host = pathdata[0]
        file = pathdata[1]

        if not host or not file:
            raise DTP_MissingData

        host_path = os.path.abspath(os.path.join(self.folder, host))
        file_path = os.path.abspath(os.path.join(host_path, file))

        if self.tounix(os.path.join(self.folder, host)) not in file_path:
            raise DTP_Unauthorized

        elif not os.path.isdir(host_path):
            raise DTP_NoSuchHost

        elif not os.path.isfile(file_path):
            raise DTP_NoSuchFile

        # Read file data
        if os.path.getsize(file_path) >= self.max_mem or (psutil.virtual_memory().available - 2048) < (2 * (1024 ** 2)):
            return f"The specified file is too large to read.\nThe server limit is: {self.max_mem} bytes"

        with open(file_path, "rb") as file:
            data = file.read()

        # Send data
        return data  # Trailing new line
