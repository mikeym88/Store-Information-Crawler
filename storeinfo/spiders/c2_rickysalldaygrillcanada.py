import scrapy
import json
from scrapy.spiders import Spider
from scrapy.http import Request
from storeinfo.items import StoreItem
from html5lib import html5parser
import json


class rickysalldaygrillcanada(scrapy.Spider):
    name = 'rickysalldaygrillcanada'

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        url = 'https://rickysrestaurants.ca/wp-admin/admin-ajax.php?action=location_search&lat=49.26544&lng=-123.00573&max_results=15&search_radius=50&searchEvent=true'
        yield Request(url=url, headers=headers, callback=self.parse_stores)

    def parse_stores(self, response):  # Renamed this to parse_stores
        stores = json.loads(response.body)
        for store in stores:
            item = StoreItem()
            item['store_name'] = store["location"]
            item['store_number'] = store["id"]
            item['address'] = store["address"]
            item['address2'] = store["address2"]
            item['city'] = store["city"]
            item['state'] = store["state"]
            item['zip_code'] = store["zip"]
            item['country'] = store["country"]
            item['phone_number'] = store["phone"]
            item['latitude'] = float(store["lat"])
            item['longitude'] = float(store["lng"])

            # Extract store hours
            hours_xpath = scrapy.Selector(text=store["hours"]).xpath("//tr")
            hours_dict = {}
            for i in hours_xpath:
                day = i.xpath(".//td[1]/text()").get()
                if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    day_hours = i.xpath(".//time/text()").get()
                    hours_dict[day] = day_hours.split(' - ')
            hours = []
            for day in hours_dict.keys():
                day_hours = day[0:3] + ": " + hours_dict[day][0] + "-" + hours_dict[day][1]
                hours.append(day_hours)
            item['store_hours'] = ", ".join(hours)

            yield item
