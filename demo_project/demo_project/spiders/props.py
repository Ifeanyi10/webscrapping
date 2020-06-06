import scrapy
import requests

class PropertySpider(scrapy.Spider):
    name = 'props'

    allowed_domains = ['tiganoproperties.com']

    start_urls = ['https://tiganoproperties.com/']

    base_url = 'https://tiganoproperties.com/'
    propTitle = ""
    propCostValue = ""
    propCostType = ""
    propImgURL = []
    prop_url = ""

    def parse(self, response):

        all_properties = response.xpath("//div[@class='figure-block']")

        for prop in all_properties:
            global prop_url
            prop_url = prop.xpath(".//a[@class='hover-effect']/@href").extract_first()
            yield scrapy.Request(prop_url, callback=self.parse_props)

    def parse_props(self, response):
        print ("New Function Called!!!")
        global propImgURL
        global propTitle
        global propCostValue
        global propCostType
        propImgURL = []

        title_div = response.xpath("//div[@class='table-cell']")
        propTitle = title_div.xpath(".//h1/text()").extract_first()

        cost_div = response.xpath("//div[@class='header-right']")
        propCostValue = title_div.xpath(".//span[@class='item-price']/text()").extract_first()

        type_li = response.xpath("//ul[@class='list-three-col']")
        propCostType = type_li.xpath(".//li[@class='prop_status']/text()").extract_first()

        all_img_div = response.xpath("//div[@class='gallery-inner']")
        all_img_items = all_img_div.xpath("//div[@class='item']")
        for item in all_img_items:
            imgURL = item.xpath("./img/@src").extract_first()
            propImgURL.append(imgURL)

        yield{
            'propTitle': propTitle,
            'propCostValue': propCostValue,
            'propCostType': propCostType,
            'propImgURL': propImgURL
        }
