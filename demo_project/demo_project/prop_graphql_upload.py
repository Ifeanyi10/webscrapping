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

        if propCostType == 'For Sale':
            propCostType = 'Sale'
        if propCostType == 'For Rent':
            propCostType = 'Rent'

        self.upload()

        yield{
            'propTitle': propTitle,
            'propCostValue': propCostValue,
            'propCostType': propCostType,
            'propImgURL': propImgURL,
            'propAdd': prop_url
        }


    def upload(self):

        query = """
                mutation{
                  createProperty(input:{title: %propTitle,
                    location:{city:"",
                      state:"Lagos"},
                    costValue: %propCostValue,
                    costType:%propCostType,
                    featured:true,
                    images: %propImgURL,
                  description: %prop_url
                  })
                }
                """

        DBurl = "https://zanga-api.now.sh/"

        access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyNTgyNzk3OTU2MTIxODkyMDQiLCJpYXQiOjE1OTE0ODE3NTEsImV4cCI6MTU5NDA3Mzc1MX0.K8_LWER2z4CqygDsD2_6utLKHyMwISqyY5SiA5Yc2ak"
        headers = {
            "token": access_token
        }


        request = requests.post(DBurl, json={'query': query}, headers=headers)
        if request.status_code == 200:
            print ("Successful")
            #return request.json()
        else:
            print ("Not Successful")
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
