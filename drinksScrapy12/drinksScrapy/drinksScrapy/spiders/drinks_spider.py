import scrapy
import random


class DrinksSpiderSpider(scrapy.Spider):
    name = "drinks_spider"
    allowed_domains = ["whiskyshop.com"]
    start_urls = ["https://www.whiskyshop.com/catalogsearch/result?string=&lb.f%5B%5D=Availability%20Values%3AIn%20Stock"]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={"User-Agent": random.choice(self.user_agents)}, callback=self.parse)

    def parse(self, response):
        for products in response.css("div.product-item-info"):
            yield {
                "name" : products.css("a.product-item-link::text").get(),
                "price" : products.css("span.price::text").get(),
                "link" : products.css("a.product-item-link::text").attrib["href"],
            }
