import logging

from pastebinParser import PastebinParser
from parsers.slexyParser import SlexyParser


class PhParser():

    def __init__(self):
        logging.info("Init parsers")
        self.parsers = [PastebinParser("https://scrape.pastebin.com/api_scraping.php?limit=100",
                                       120,
                                       "Pastebin"),
                        SlexyParser("https://slexy.org/recent",
                                    120,
                                    "Slexy")
                        ]

    def run(self):

        rets = []

        for parser in self.parsers:
            try:
                ret = parser.run()
            except Exception as e:
                logging.error("Parser %s crashed, %s", parser.name, e)
                ret = None
            if ret:
                rets.append(ret)

        return rets
