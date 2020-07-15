from __future__ import unicode_literals
import scrapy
import string


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
                "Name": cells[0].xpath("./text()").get(),
                "Location": cells[1].xpath("./text()").get().title(),
                "Region": region,
                "MAAC Club URL": maac_url
            }

            yield scrapy.Request(maac_url, callback=self.parse_maac_club_page, meta={"general_info": general_info})

    def parse_maac_club_page(self, response):
        contact_xpath = '//p[./strong[contains(text(), "Club Contact:") or contains(text(), "Club Contacts:")]]/text()'
        response_1 = response.meta["general_info"]
        response_2 = {
            "contact": response.xpath(contact_xpath).get(),
            "url_1": response.xpath('//p[./strong[contains(text(), "Website:")]]/a/text()').get(),
            "url_2": response.xpath('//p[./strong[contains(text(), "Website:")]]/a/@href').get()
        }
        if response_2["contact"]:
            response_2["contact"] = response_2["contact"].strip().title()
        if response_2["url_1"]:
            response_2["url_1"] = response_2["url_1"].lower().strip()
        if response_2["url_2"]:
            response_2["url_2"] = response_2["url_2"].lower().strip()
            if response_2["url_2"] == response_2["url_1"]:
                response_2["url_2"] = None
        results = response_1.copy()   # start with x's keys and values
        results.update(response_2)
        # TODO: find out why {**x, **y} does not work
        yield results
