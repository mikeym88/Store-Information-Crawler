from __future__ import unicode_literals
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from storeinfo.items import StoreItem


class towncaredentalSpider(scrapy.Spider):
    name = "towncaredental"
    start_urls = ['https://www.towncaredental.com/locations/']

    def parse(self, response):
        stores = response.xpath('//li[@data-id]')
        for store in stores:
            item = StoreItem()
            item['store_name'] = store.xpath('.//h3/a/span/text()').extract_first().strip().replace("\u00a0", " ")
            address = store.xpath('.//*[@class="address"]/text()').getall()
            item['address'] = ', '.join(address[0:-1]).strip()

            city_state_zip_info = address[-1].split(',')
            item['city'] = city_state_zip_info[0]
            item['state'] = city_state_zip_info[1].split()[0]
            item['zip_code'] = city_state_zip_info[1].split()[1]
            item['country'] = 'US'
            item['phone_number'] = store.xpath('.//*[@class="contact"]/a/text()').extract_first()

            yield item
