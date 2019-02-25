import logging

from pastebinParser import PastebinParser
from parsers.slexyParser import SlexyParser
from parsers.gistParser import GistParser

logger = logging.getLogger("logger")


class PhParser():

    def __init__(self):
        logger.info("Init parsers")
        self.parsers = [PastebinParser("https://scrape.pastebin.com/api_scraping.php?limit=100",
                                       120,
                                       "Pastebin"),
                        SlexyParser("https://slexy.org/recent",
                                    120,
                                    "Slexy"),
                        GistParser('https://gist.github.com/discover',
                                   60,
                                   'Gist')
                        ]

    def run(self):

        rets = []

        for parser in self.parsers:
            try:
                ret = parser.run()
            except Exception as e:
                logger.error("Parser %s crashed, %s", parser.name, e)
                ret = None
            if ret:
                rets.append(ret)

        return rets
