from __future__ import unicode_literals
import scrapy
from scrapy.http import Request
import random


class MarketWatchSpider(scrapy.Spider):
    name = "marketwatch_ipo"

    def start_requests(self):
        random.seed()
        headers = [
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-CA,en;q=0.9,ro-RO;q=0.8,ro;q=0.7,en-GB;q=0.6,en-US;q=0.5",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "DNT": 1,
                "Host": "www.marketwatch.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": 1,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
            },
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-CA,en;q=0.9,ro-RO;q=0.8,ro;q=0.7,en-GB;q=0.6,en-US;q=0.5",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "DNT": 1,
                "Host": "www.marketwatch.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": 1,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            }
        ]

        url = 'https://www.marketwatch.com/tools/ipo-calendar'
        yield Request(url=url, headers=random.choice(headers))

    def parse(self, response):
        entries = response.xpath('//div[contains(@data-tab-pane,"Upcoming Ipos")]//tr[@class="table__row" and //td[@class="table__cell"]]/td[2]/text()')
        symbols = {"symbols": []}
        for symbol in entries.getall():
            symbols["symbols"].append(symbol)
        yield symbols
