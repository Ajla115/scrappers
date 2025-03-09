import scrapy
#from fake_useragent import UserAgent


class PhoneCaseSpider(scrapy.Spider):
    name = "phone_case_spider"
    start_urls = ["https://olx.ba/pretraga?q=iphone+13+maska+za+telefon"]

    #ua = UserAgent()


    def parse(self, response):
        for product in response.css("div.w-full.flex.cardd"):  # Corrected class selector
            yield {
                "name": product.css("h1.main-heading::text").get(),
                "price": product.css("span.price::text").get(),  # Adjust based on inspection
                "link": product.css("a::attr(href)").get(),
                "source": "Olx.ba"
            }
