import scrapy
from scrapy.http import FormRequest
from storeinfo.items import CompanyItem
import string

class UAESpider(scrapy.Spider):
    name = 'uae_free'
    headers = {
        'X-MicrosoftAjax': 'Delta=true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
    }

    base_url = "https://www.uaeonlinedirectory.com/"

    start_urls = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=%s' % x
                  for x in string.ascii_uppercase]

    allowed_domains = ['www.uaeonlinedirectory.com']
    # TODO: Include the urls for all other items (e.g. A-Z)

    def __init__(self, item=None):
        super(UAESpider, self).__init__()
        if item:
            if len(item) != 1 or item not in string.ascii_letters:
                raise ValueError("Parameter 'item' must be a letter")
            else:
                self.start_urls = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=%s' % item.upper()]

    def parse(self, response):
        # request the next page
        if "page" in response.meta.keys():
            current_page = response.meta["page"] + 1
        else:
            current_page = 1

        if current_page == 1:
            # submit a form (first page)
            data = {}
            for form_input in response.css('form#aspnetForm input'):
                name = form_input.xpath('@name').extract()[0]
                try:
                    value = form_input.xpath('@value').extract()[0]
                except IndexError:
                    value = ""
                data[name] = value
            data['__EVENTTARGET'] = 'ctl00$MainContent$List'
            data['__EVENTARGUMENT'] = 'Page$1'
        else:
            # Extract the form fields and arguments using XPATH
            event_validation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()
            view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
            view_state_generator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()
            view_state_encrypted = response.xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()

            data = {
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$grdDirectory',
                '__EVENTARGUMENT': 'Page$%d' % current_page,
                '__EVENTVALIDATION': event_validation,
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_state_generator,
                '__VIEWSTATEENCRYPTED': view_state_encrypted,
                '__ASYNCPOST': 'true',
                '': ''
            }

        # Yield the companies
        # TODO: move this to a different function
        rows = response.xpath('//tr[@class="GridViewRowStyle"]')
        for row in rows:
            company = CompanyItem()
            company['company'] = row.xpath('.//td[2]//text()').get()
            company['company_link'] = self.base_url + row.xpath('.//td[2]//a/@href').get()
            company['po_box'] = row.xpath('.//td[3]//text()').get()
            company['phone_number'] = row.xpath('.//td[5]//text()').get()
            zone = row.xpath('.//td[4]//text()').get()
            if zone == "\u00a0":
                zone = None
            company['zone'] = zone
            company['category'] = row.xpath('.//td[6]//text()').get()
            if row.xpath('.//td[6]//a/text()').get():
                company['category_link'] = self.base_url + row.xpath('.//td[6]//a/@href').get()
            else:
                company['category_link'] = None
            yield company
        else:
            new_request = FormRequest(url=response.request.url,
                                      method='POST',
                                      formdata=data,
                                      callback=self.parse,
                                      meta={'page': current_page},
                                      dont_filter=True,
                                      headers=self.headers)

            # Check if the last page has been reached
            last_page_number = response.xpath(
                '(//table[@class="GridViewStyle"]//tr[@class="numbering"]//table//a)[last()]/text()'
            ).get()
            current_page_number = response.xpath(
                '//table[@class="GridViewStyle"]//tr[@class="numbering"]//table//span/text()'
            ).get()

            # Continue only if there are more pages to be scraped
            if last_page_number == ">>":
                yield new_request
            elif int(current_page_number) < int(last_page_number):
                yield new_request
