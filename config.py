import sys
import configparser
import logging
import logging.handlers
from clockwork import clockwork

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p")

logger = logging.getLogger("logger")

logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler("pastehunter2.log",
                                               maxBytes=100000,
                                               backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))

logger.addHandler(handler)
logger.propagate = False

config = configparser.ConfigParser()
logger.info("Reading config.ini, fields are not checked!")
config.read("./config.ini")

if not config.sections():
    logger.error("Config file seems empty or missing!")
    sys.exit()

clockworkapi = clockwork.API(config["clockwork"]["api"])
