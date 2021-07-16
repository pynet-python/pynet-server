# Copyright 2021 iiPython

# Modules
import sys
from rich.console import Console

# Initialization
console = Console()

# Crash handler
def exit(code: int, message):
    message = str(message)

    # Log
    console.log(message)

    # Exit script
    sys.exit(code)

console.exit = exit
