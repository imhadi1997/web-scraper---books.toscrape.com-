#       ustaad's code
import scrapy
import csv


class BooksSpiderSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def start_requests(self):

        #   Add urls of any category from here https://books.toscrape.com/ by selectiong books column
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
        ]

        for url in urls:
            yield scrapy.Request(
                url=url, callback=self.product_page, headers=self.headers
            )

    def product_page(self, response):
        all_products = response.xpath(
            '//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]'
        )
        for product in all_products:
            title = product.xpath(".//h3/a/@title").get()
            price = (
                product.xpath(
                    './/div[@class="product_price"]/p[@class="price_color"]/text()'
                )
                .get()
                .strip()
            )
            rating = (
                product.xpath('.//p[contains(@class,"star-rating")]/@class')
                .get()
                .split()[-1]
                .strip()
            )
            stock_status = "".join(
                [
                    character.strip()
                    for character in product.xpath(
                        './/p[@class="instock availability"]//text()'
                    ).extract()
                    if character != ""
                ]
            )
            yield {
                "title": title,
                "price": price,
                "rating": rating,
                "stock_status": stock_status,
            }

