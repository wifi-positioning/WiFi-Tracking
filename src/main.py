#!/usr/bin/env python3
from arg_parser import ArgParser
from config_working.config_parser import ConfigParser

# Extract config file path from cli args
config_file = ArgParser().parse_args()

# Make config instance from received json file
config = ConfigParser().parse_config(config_file)