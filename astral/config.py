import os
import configparser

config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "common", "config.ini"))
config = configparser.ConfigParser()
config.read(config_file)