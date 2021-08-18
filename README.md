# PyNet Server
---

### Introduction
Servers are the base of PyNet, acting like HTTP servers but distributing [DTP](https://github.com/pynet-python/protodtp) responses.
To setup a PyNet server you can follow this guide, although this provides a very basic setup.

### Dependencies
PyNet is built using Python and a few python packages; you will also require git in order to clone this repository. You can install all of this with the following command:

`$ sudo apt install git python3 python3-pip && python3 -m pip install -r reqs.txt`

### Setup
Clone the server repository with:

`$ git clone https://github.com/pynet-python/pynet-server`


To configure your server, you need to create a `config.json` file.
The inside of it should look like the following:
```json
{"port": 8282, "filestore": "$HOME/.dtp", "max_mem": "20mb"}
```

- "port" should be a integer describing what port the PyNet server should run on;
- "filestore" is a path to a folder (that exists or will be created) for storage of files;
- "max_mem" is the maximum amount of **system memory** that a DTP request can use;

### Launching
You can launch the PyNet server like any Python file, eg.:
`python3 start.py`

Now that you have the server setup, it is recommended to also setup and configure
the webserver, more info [here](https://github.com/pynet-python/pynet-ws).
