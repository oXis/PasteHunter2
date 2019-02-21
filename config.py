import sys
import configparser
import logging
from clockwork import clockwork

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p")

config = configparser.ConfigParser()
logging.info("Reading config.ini, fields are not checked!")
config.read("./config.ini")

if not config.sections():
    logging.error("Config file seems empty or missing!")
    sys.exit()

clockworkapi = clockwork.API(config["clockwork"]["api"])
