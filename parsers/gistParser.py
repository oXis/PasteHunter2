#!/usr/bin/python3
import copy
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from parsers.emptyParser import EmptyParser, template


class GistParser(EmptyParser):

    def getContent(self):

        response = requests.get(self.apiUrl)
        ret = []

        html_soup = BeautifulSoup(response.text, "lxml")

        for a in html_soup.find_all("a", class_="link-overlay"):
            tmp = copy.copy(template)
            tmp["user"] = a["href"].split('/')[-2]
            tmp["title"] = "None"
            tmp["full_url"] = a["href"]

            tmp["key"] = a["href"].split('/')[-1]

            response = requests.get(tmp["full_url"])
            html_soup2 = BeautifulSoup(response.text, "lxml")

            for a2 in html_soup2.find_all("a"):
                if "raw" in a2["href"]:
                    tmp["scrape_url"] = urljoin(self.apiUrl, a2["href"])
                    break # no need to keep going

            ret.append(tmp)

        return ret
