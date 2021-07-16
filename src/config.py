# Copyright 2021 iiPython (Benjamin O'Brien)

# Modules
import os
import json
import shutil
from src.console import console

# Initialization
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
_config_file = os.path.join(_root_dir, "config.json")

# Load configuration
if not os.path.isfile(_config_file):
    console.exit(1, "[red]No config.json file to use!")

try:
    with open(_config_file, "r") as file:
        config = json.loads(file.read())

except Exception:
    console.exit(1, "[red]config.json is invalid!")

# Configuration class
class Configuration(object):
    def __init__(self, data: dict = {}):
        self.data = data

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, accept = None, min: int = 0, default = None):
        if key in self.data:

            # Grab value
            value = self.data[key]

            # Check for accept
            if accept is not None:
                if not isinstance(value, accept):
                    return console.exit(1, "[red]'{}' in config.json needs to be of type: '{}'".format(key, str(accept)))

                # Check for min
                if type(value) in [int, float] and min is not None:
                    if value < min:
                        return console.exit(1, "[red]'{}' in config.json must be at least {}".format(key, min))

            return self.data[key]

        if default is not None:
            return default

        return console.exit(1, "[red]config.json missing required field: '{}'".format(key))

config = Configuration(config)

# Ensure filestore exists
fstore_path = config.get("filestore", accept = str)
if not os.path.isdir(fstore_path):
    os.mkdir(fstore_path)

# Copy config file
shutil.copyfile(
    os.path.abspath(
        os.path.join(
            os.path.join(os.path.dirname(__file__), ".."),
            "config.json"
        )
    ),
    os.path.join(
        fstore_path,
        "config.json"
    )
)
