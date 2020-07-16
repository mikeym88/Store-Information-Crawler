import scrapy
import json
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from storeinfo.items import StoreItem


class JockeySpider(scrapy.Spider):
    name = "jockey"
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    def start_requests(self):
        url = 'https://www.jockey.com/shoppingguide/storelocator'
        yield Request(url=url, headers=self.headers, callback=self.parse_stores)

    def parse_stores(self, response):
        embeddedJSON = response.xpath('//main/script').re_first('\{allStores:.*\]\}')
        embeddedJSON = embeddedJSON.replace("{allStores:", "")[0:-1]

        stores = json.loads(embeddedJSON)
        for store in stores:
            item = StoreItem()
            item['store_name'] = store['StoreName'].strip()
            item['store_number'] = store['StoreId']
            item['store_uid'] = store['StoreCode']
            item['address'] = store['AddressLine1']
            item['address2'] = store['AddressLine2']
            item['city'] = store['City']
            item['state'] = store['State']
            item['zip_code'] = store['PostalCode']
            item['country'] = store['CountryCode']
            item['phone_number'] = store['MainPhone']
            item['latitude'] = float(store['Latitude'])
            item['longitude'] = float(store['Longitude'])
            item['store_hours'] = store['Hours']

            yield item
