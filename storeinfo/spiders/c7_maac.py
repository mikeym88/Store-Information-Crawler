from __future__ import unicode_literals
import scrapy
import string
import re

class MaacClubSpider(scrapy.Spider):
    name = "maac"
    index = string.ascii_uppercase.index("M") + 1
    base = "https://www.maac.ca/en/"
    start_urls = ['https://www.maac.ca/en/clubs_by_zone.php?zone_code=%s' % x for x in string.ascii_uppercase[:index]]

    def parse(self, response):
        region = response.xpath('//select[@name="zone_code"]/option[@selected]/text()').get()
        rows = response.xpath('//table[@class="data_table"]//tr[@class="odd" or @class="even"]')
        for r in rows:
            cells = r.xpath("./td")
            maac_url = self.base + cells[2].xpath("./a/@href").get()

            general_info = {
                "Name": cells[0].xpath("./text()").get().title(),
                "Location": cells[1].xpath("./text()").get().title(),
                "Region": region,
                "MAAC Club URL": maac_url
            }

            yield scrapy.Request(maac_url, callback=self.parse_maac_club_page, meta={"general_info": general_info})

    def parse_maac_club_page(self, response):
        contact_xpath = '//p[./strong[contains(text(), "Club Contact:") or contains(text(), "Club Contacts:")]]/text()'
        general_info = response.meta["general_info"]
        specific_info = {
            "Contact(s)": response.xpath(contact_xpath).get(),
            "url_1": response.xpath('//p[./strong[contains(text(), "Website:")]]/a/text()').get(),
            "url_2": response.xpath('//p[./strong[contains(text(), "Website:")]]/a/@href').get()
        }
        if specific_info["Contact(s)"]:
            specific_info["Contact(s)"] = specific_info["Contact(s)"].strip().title()
        if specific_info["url_1"]:
            specific_info["url_1"] = specific_info["url_1"].lower().strip()
        if specific_info["url_2"]:
            specific_info["url_2"] = specific_info["url_2"].lower().strip()
            if specific_info["url_2"] == specific_info["url_1"]:
                specific_info["url_2"] = None
        info = general_info.copy()   # start with x's keys and values
        info.update(specific_info)
        # TODO: find out why {**x, **y} does not work
        yield info

        airfields_table_xpath = '//table[contains(.//th/text(), "Club Airfields")]//tr[@class="odd" or @class="even"]'
        airfields = response.xpath(airfields_table_xpath)
        for field in airfields:
            club = general_info["Name"]  # Or this xpath can be used:
            name = field.xpath('.//td/p/strong/text()').get()
            coordinates = field.xpath('.//iframe/@src').get()
            coordinates = re.search("(\?|\&)q=(?P<latitude>-?(\d|\.)+),(?P<longitude>-?(\d|\.)+)", coordinates)
            if coordinates:
                latitude = float(coordinates.group('latitude'))
                longitude = float(coordinates.group('longitude'))
                skyvector = "https://skyvector.com/?ll=%f,%f&zoom=1" % (latitude, longitude)
                google_maps = "http://google.com/maps?q=%f,%f" % (latitude, longitude)
                bing_maps = "https://www.bing.com/maps?q=%f,%f" % (latitude, longitude)
            else:
                latitude = None
                longitude = None
                skyvector = None
                google_maps = None
                bing_maps = None
            airfield_type = field.xpath('.//td/p[starts-with(text(), "Type: ")]/text()').get()
            if airfield_type:
                airfield_type = airfield_type.replace("Type: ", "")
            yield {
                "Club": club.title(),
                "Airfield Name": name.title(),
                "Type": airfield_type,
                "Latitude": latitude,
                "Longitude": longitude,
                "Skyvector Maps": skyvector,
                "Google Maps": google_maps,
                "Bing Maps": bing_maps
            }
