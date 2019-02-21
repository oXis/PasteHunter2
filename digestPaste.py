import os
import logging
import re
import json

from report import Report


class Filter():

    def __init__(self, ftype, kargs):

        self.ftype = ftype

        for key, value in kargs.items():
            if key == "urgent":
                value = bool(value)
            elif key == "regex":
                value = re.compile(value)

            setattr(self, key, value)


# pylint: disable=R0201
class DigestPaste():

    def __init__(self, filterFile):

        self.filterFile = filterFile
        self.filters = self.loadFilters()
        self.filterFileTime = os.path.getmtime(filterFile)

    def check(self, item):
        try:
            assert "regex" in item
            assert "desc" in item
            assert "urgent" in item
        except AssertionError:
            logging.error("Error while parsing filters.json, \
                          one item is not correctly declared!")
            return False

        return True

    def loadFilters(self):

        filters = []

        with open(self.filterFile, 'r') as fin:
            try:
                jsonFilters = json.loads(fin.read())
            except json.decoder.JSONDecodeError as e:
                logging.error("Malformed json file %s", e)
                return filters

            for ftype in jsonFilters:
                for item in jsonFilters[ftype]:
                    if self.check(item):
                        filters.append(Filter(ftype, item))

        return filters

    def update(self):

        filterFileNewTime = os.path.getmtime(self.filterFile)
        if filterFileNewTime > self.filterFileTime:
            logging.info("Filter file reloaded.")
            self.filters = self.loadFilters()
            self.filterFileTime = os.path.getmtime(self.filterFile)

    def digest(self, paste):

        parser = paste["parser"]
        pId = parser.getId(paste)

        logging.info("\t[*] Paste %s from %s",
                     pId,
                     paste["parser"].name)

        content = parser.getPasteContent(paste)

        matches = self.analyse(content)

        if matches:
            for f in matches:
                logging.warning("Paste %s matches filter %s with %s",
                                pId, f.ftype, f.desc)

            return Report(paste, content, matches)

        return None

    def analyse(self, content):

        contentLower = content.lower()
        filtersMatched = []

        for f in self.filters:
            if re.search(f.regex, contentLower):
                filtersMatched.append(f)

        return filtersMatched
