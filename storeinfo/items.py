# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StoreItem(Item):
    store_name = Field()
    store_number = Field()
    store_uid = Field()
    address = Field()
    address2 = Field()
    city = Field()
    state = Field()
    zip_code = Field()
    country = Field()
    phone_number = Field()
    latitude = Field()
    longitude = Field()
    store_hours = Field()
    other_fields = Field()
    attributes = Field()
    adminattributes = Field()
    store_type = Field()
    coming_soon = Field()
    chain_id = Field()
    scrape_id = Field()
    hash_primary = Field()
    hash_secondary = Field()
    distributor_name = Field()
    closed = Field()
    geo_accuracy = Field()


class CompanyItem(Item):
    company = Field()
    company_link = Field()
    zone = Field()
    category = Field()
    category_link = Field()
