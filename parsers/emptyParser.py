import time
import logging
import requests

template = {"scrape_url": '',
            "full_url": '',
            "date": '',
            "key": '',
            "size": '',
            "expire": '',
            "title": '',
            "syntax": '',
            "user": ''}


# pylint: disable=R0201
class EmptyParser():

    def __init__(self, apiUrl, maxTime, name):

        self.apiUrl = apiUrl
        self.maxTime = maxTime
        self.timeLast = maxTime
        self.timeCurrent = 0

        self.name = name

        self.lastPasteList = {}

    def getContent(self):
        # TO IMPLEMENT
        response = ""
        return response

    def getLastPaste(self):

        # Implement a scrape function to return a paste in that format
        # {
        #      "scrape_url": URL of RAW paste,
        #      "full_url": URL of the paste,
        #      "date": "1442911802",
        #      "key": "0CeaNm8Y",
        #      "size": "890",
        #      "expire": "1442998159",
        #      "title": "Once we all know when we goto function",
        #      "syntax": "java",
        #      "user": "admin"
        # }

        response = self.getContent()

        keys = [r["key"] for r in response]
        newPasteList = set(keys).difference(self.lastPasteList)
        oldPastList = set(keys).intersection(self.lastPasteList)

        self.lastPasteList = oldPastList.union(newPasteList)

        logging.info("%s - %s new paste(s)", self.name, len(newPasteList))

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
            logging.error("Cannot decode %s for parser %s", pasteJson["key"], self.name)
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
