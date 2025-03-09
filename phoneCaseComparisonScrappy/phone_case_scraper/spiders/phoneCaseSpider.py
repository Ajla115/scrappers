import scrapy


class PhoneCaseSpider(scrapy.Spider):
    name = "phone_case_spider"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for product in response.css("article.peoduct_pod"):
            yield {
                "name" : product.css("h3::text").get(),
                #"price" :
               # "link" :
                "source" : "Olx.ba",
            }
