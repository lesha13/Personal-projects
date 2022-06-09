# importing libraries


from bs4 import BeautifulSoup
from random import choice
import requests
import re

from stocks_adapter import Adapter


class Crawler:

    def __init__(self):
        """
        Initialization,
        making set objects to store sites,
        using adapter from stocks_adapter.py file,
        """
        self.new_pages = set()
        self.used_pages = set()
        self.adapter = Adapter()

    @staticmethod
    def get_page(url):
        """
        Function, that returns BeautifulSoup obj of page if it's possible
        :param url: page url
        :return: BeautifulSoup obj
        """
        try:
            html = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        if html.status_code == 404:
            return None
        else:
            return BeautifulSoup(html.text, "html.parser")

    def crawl(self, url):
        """
        Function, that gets needed data from the page and writes it to the database,
        than crawls next page from "People also view" and so on
        :param url: url to get data from
        :return: self
        """
        url = "https://finance.yahoo.com" + url[url.find("/quote/"):url.find("?p="):]
        self.new_pages.add(url)
        for _ in range(1000):   # 1000 because i don't want it to run forever
            print(f"Now on: {url}")
            bs = self.get_page(url)
            self.used_pages.add(url)

            if bs is not None:

                try:
                    ticker = bs.h1.text
                    price = float(bs.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text.replace(",", ""))
                except AttributeError:
                    self.adapter.write_data("smth wrong :/", 0, "smth wrong :/")
                else:
                    self.adapter.write_data(ticker, price, url)
                    for __ in bs.find_all(
                            "a", {"href": re.compile(r"^((/quote/)([A-Z])*(\?p=)([A-Z])*(&ncid=yahooproperties_).*)$")}):
                        self.new_pages.add("https://finance.yahoo.com/quote/" + __.text)

            else:
                print(f"{url} - Access denied :/")

            url = choice(list(self.new_pages ^ self.used_pages))

        return self

    def __str__(self):
        return f"Crawler"

    def __del__(self):
        pass
