import scrapy
from scrapy.http import FormRequest


class UAESpider(scrapy.Spider):
    name = 'uae_free'
    headers = {
        'X-MicrosoftAjax': 'Delta=true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
    }

    allowed_domains = ['www.uaeonlinedirectory.com']
    # TODO: Include the urls for all other items (e.g. A-Z)
    current_page = 0

    def __init__(self, item='A'):
        super(UAESpider, self).__init__()
        self.start_urls = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=%s' % item]

    def parse(self, response):
        # request the next page
        self.current_page = self.current_page + 1

        if self.current_page == 1:
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
                '__EVENTARGUMENT': 'Page$%d' % self.current_page,
                '__EVENTVALIDATION': event_validation,
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_state_generator,
                '__VIEWSTATEENCRYPTED': view_state_encrypted,
                '__ASYNCPOST': 'true',
                '': ''
            }

        # Yield the companies
        # TODO: move this to a different function
        rows = response.xpath('//table[@class="GridViewStyle"]//tr')
        for row in rows[1:11]:
            result = {
                'company_name': row.xpath('.//td[2]//text()').get(),
                'company_name_link': row.xpath('.//td[2]//a/@href').get(),
                'zone': row.xpath('.//td[4]//text()').get(),
                'category': row.xpath('.//td[6]//text()').get(),
                'category_link': row.xpath('.//td[6]//a/@href').get()
            }
            print(result)
            yield result
        else:
            new_request = FormRequest(url=response.request.url,
                                      method='POST',
                                      formdata=data,
                                      callback=self.parse,
                                      meta={'page': self.current_page},
                                      dont_filter=True,
                                      headers=self.headers)
            # TODO: check if there is a next page or if it is the last one, and only yield if there is one

            yield new_request
