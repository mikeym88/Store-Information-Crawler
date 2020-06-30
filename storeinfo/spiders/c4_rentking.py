import scrapy
import json
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from storeinfo.items import StoreItem
import pdb
import re


class RentkingSpider(scrapy.Spider):
    name = "rentking"
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    def start_requests(self):
        url = 'https://www.myrentking.com/store_finder.html'
        yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # A JSON object of all the store locations was available within a Script tag in the website's HTML source.
        stores = response.xpath('//body/script[contains(text(), "// Create a JSON array of all possible locations")]')
        stores = stores.re_first('\[[\s\S]*\{"store_name":[^\]]*\];')
        stores = re.sub(",( |\r|\n)*\];", "]", stores)
        stores = json.loads(stores)
        for store in stores:
            url = store['url']
            item = StoreItem()
            item['store_name'] = store['store_name'].strip()
            item['address'] = store['address']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            yield Request(url=response.urljoin(url),
                          headers=self.headers,
                          callback=self.parse_store,
                          meta={'item': item})

    def parse_store(self, response):
        item = response.meta['item']

        # Extract store hours and store phone number, which are located on another page
        # To do this we follow the link to the specific store and extract the information

        # Extract phone number
        item['phone_number'] = response.xpath('//*[@id="location-address-section"]/strong/text()')\
            .extract_first().strip()

        # Extract store hours
        hours_xpath = response.xpath('(//div[@id="location-hours-section"])[1]//tr')
        hours_dict = {}
        for row in hours_xpath:
            day = row.xpath(".//td[1]/text()").get()
            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                day_hours = row.xpath(".//td[2]/text()").get().strip()
                hours_dict[day] = day_hours.split('-')
        hours = []
        for day in hours_dict.keys():
            if len(hours_dict[day]) > 1:
                day_hours = day[0:3] + ": " + hours_dict[day][0] + "-" + hours_dict[day][1]
            else:
                day_hours = day[0:3] + ": " + hours_dict[day][0]
            hours.append(day_hours)
        item['store_hours'] = ", ".join(hours)

        yield item
