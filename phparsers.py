import logging

from pastebinParser import PastebinParser


class PhParser():

    def __init__(self):
        logging.info("Init parsers")
        self.parsers = [PastebinParser(
                        "https://scrape.pastebin.com/api_scraping.php?limit=50",
                        10,
                        "Pastebin")
                        ]

    def run(self):

        rets = []

        for parser in self.parsers:
            ret = parser.run()
            if ret:
                rets.append(ret)

        return rets
