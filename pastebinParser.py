import time
import logging
import requests

logger = logging.getLogger("logger")


# pylint: disable=R0201
class PastebinParser():

    def __init__(self, apiUrl, maxTime, name):

        self.apiUrl = apiUrl
        self.maxTime = maxTime
        self.timeLast = maxTime
        self.timeCurrent = 0

        self.name = name

        self.lastPasteList = {}

    def getLastPaste(self):
        try:
            # poll the Pastebin API
            response = requests.get(self.apiUrl)
        except Exception as e:
            logger.warning("%s error -> %s", self.name, e)

        response = response.json()

        keys = [r["key"] for r in response]
        newPasteList = set(keys).difference(self.lastPasteList)
        oldPastList = set(keys).intersection(self.lastPasteList)

        self.lastPasteList = oldPastList.union(newPasteList)

        logger.info("%s - %s new paste(s) - Next pull in %s seconds",
                    self.name, len(newPasteList), self.maxTime)

        ret = []
        for p in response:
            if p["key"] in newPasteList:
                p["parser"] = self
                ret.append(p)

        return ret

    def getPasteContent(self, pasteJson):

        paste = requests.get(pasteJson["scrape_url"])

        try:
            paste = paste.content.decode('utf-8')
        except UnicodeDecodeError:
            logger.error("Cannot decode %s for parser %s", pasteJson["key"], self.name)
            paste = ""

        return paste

    def getId(self, paste):
        return paste["key"]

    def getUser(self, paste):
        return paste["user"]

    def getURL(self, paste):
        return paste["full_url"]

    def run(self):

        self.timeCurrent = time.time()
        ret = []

        if self.timeCurrent - self.timeLast > self.maxTime:
            ret = self.getLastPaste()
            self.timeLast = time.time()

        return ret
