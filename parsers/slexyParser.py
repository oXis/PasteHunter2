#!/usr/bin/python3
import copy
import requests
from bs4 import BeautifulSoup

from parsers.emptyParser import EmptyParser, template


class SlexyParser(EmptyParser):

    def getContent(self):

        response = requests.get(self.apiUrl)
        ret = []

        html_soup = BeautifulSoup(response.text, "lxml")

        for tr in html_soup.find_all("tr", class_="row-link"):
            tmp = copy.copy(template)
            content = tr.find_all("td")
            tmp["syntax"] = content[0].text
            tmp["user"] = content[1].text
            tmp["title"] = content[2].text
            tmp["full_url"] = "https://slexy.org" + \
                content[3].find("a")["href"]

            tmp["key"] = tmp["full_url"].split('/')[-1]

            response = requests.get(tmp["full_url"])
            html_soup2 = BeautifulSoup(response.text, "lxml")

            for a in html_soup2.find_all("a"):
                if "raw" in a["href"]:
                    tmp["scrape_url"] = "https://slexy.org" + a["href"]
                    break # no need to keep going

            ret.append(tmp)

        return ret
