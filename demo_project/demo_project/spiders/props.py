import scrapy
#import requests

class PropertySpider(scrapy.Spider):
    name = 'props'

    start_urls = [
        'https://tiganoproperties.com/'
    ]

    def parse(self, response):
        for prop in response.xpath("//div[@class='figure-block']"):
            yield{
                'propTitle': prop.xpath(".//h3[@class='pull-left']/text()").extract_first(),
                'propCostValue': prop.xpath(".//div[@class='cap-price pull-left']/text()").extract_first(),
                'propCostType': prop.xpath(".//a/text()").extract_first(),
                'propImgURL': prop.xpath(".//a[@class='hover-effect']/img/@src").extract_first(),
                'propAdd': prop.xpath(".//a[@class='hover-effect']/@href").extract_first()
            }

        next_page = response.xpath(".//a[@class='hover-effect']/img/@src").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_link, callback = self.parse)
