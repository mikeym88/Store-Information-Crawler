from __future__ import unicode_literals
import scrapy
from scrapy.http import Request
import random
from datetime import datetime

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
        tabs = ["Recently Priced", "Upcoming Ipos", "Future Ipos", "Withdrawn"]
        for category in tabs:
            xpath = '//div[contains(@data-tab-pane,"%s")]//tr[@class="table__row" and //td[@class="table__cell"]]' % category
            entries = response.xpath(xpath)
            for e in entries:
                name = e.xpath("./td[1]/a/text()").get()
                if not name:
                    name = e.xpath("./td[1]/text()").get()
                link = e.xpath("./td[1]/a/@href").get()
                symbol = e.xpath('./td[2]/text()').get()
                if not symbol:
                    symbol = e.xpath('./td[2]//a/text()').get()

                exchange = e.xpath('./td[3]/text()').get()
                price_range = e.xpath('./td[4]/text()').get()
                shares = e.xpath('./td[5]/text()').get()
                if shares:
                    shares = int(shares.replace(",", ""))
                week_of = e.xpath('./td[6]/text()').get()
                if week_of:
                    week_of = datetime.strptime(week_of, "%m/%d/%Y")
                yield {
                    "Company": name,
                    "Symbol": symbol,
                    "Exchange": exchange,
                    "Price Range": price_range,
                    "Shares": shares,
                    "Week Of": week_of,
                    "Date Retrieved": datetime.now().strftime("%Y-%m-%d"),
                    "Category": category,
                    "Link": link
                }
