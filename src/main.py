#!/usr/bin/env python3
from include.arg_parser import ArgParser
from include.config_parser import ConfigParser
from engine import Engine
from signal import signal, SIGINT
from sys import exit

def signal_handler(signal, frame):
	if server_engine in globals():
		server_engine.shutdown()
	exit(1)

signal(SIGINT, signal_handler)

# Extract config file path from cli args
args = ArgParser().parse_args()

# Make config instance from received json file
config = ConfigParser().parse_config(args.config_file)
method = { "method" : args.mode }
config.update(method)

# Run server engine with config
server_engine = Engine(config)
server_engine.run()
