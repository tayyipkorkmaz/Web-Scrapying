import scrapy
from smartmaple.items import KitapYurduBooks, KitapYurduProducts


class KitapyurduSpider(scrapy.Spider):
    name = "kitapyurdu"
    allowed_domains = ["www.kitapyurdu.com"]
    start_urls = ["https://www.kitapyurdu.com/index.php?route=product/category"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "smartmaple.pipelines.KitapyurduPipeline": 300,
        }
    }

    def parse_category(self, response):
        """Parse category page and yield next page if exists"""
        self.cok_satanlar = []
        self.yeni_cikanlar = []
        books_link = response.xpath(
            '//div[@id="content"]/div/div/div/div/span/a/@href'
        ).getall()

        # Get books links
        cok_satanlar_link = books_link[0]
        yeni_cikanlar_link = books_link[1]

        yield scrapy.Request(url=cok_satanlar_link, callback=self.parse_cok_satanlar)
        yield scrapy.Request(url=yeni_cikanlar_link, callback=self.parse_yeni_cikanlar)

    def parse_cok_satanlar(self, response):
        """Parse cok_satanlar page and yield next page if exists"""
        products = response.xpath('//div[contains(@class, "product-cr")]')
        category_title = response.xpath('//div[@id="content"]/h1/text()').get()

        for product in products:
            book_name = product.xpath(
                './/div[@class="name ellipsis"]/a/span/text()'
            ).get()

            publisher = product.xpath(
                './/div[@class="publisher"]//span/a/span/text()'
            ).get()
            price = product.xpath(
                './/div[@class="price"]//div[@class="price-new "]/span[@class="value"]/text()'
            ).get()

            author_selector = product.xpath('.//div[@class="author"]//span/a/text()')
            authors = author_selector.extract()
            combined_authors = (
                " ".join(authors).strip()
                or product.xpath(
                    './/div[@class="author compact ellipsis"]/a/text()'
                ).get()
            )
            # Convert price to float
            if price:
                price = price.replace(".", "").replace(",", ".").strip()
                book_price = float(price)
            else:
                book_price = None

            # Create a dictionary for each book
            self.cok_satanlar.append(
                KitapYurduBooks(
                    book_name=book_name,
                    book_publisher=publisher,
                    book_author=combined_authors,
                    book_price=book_price,
                )
            )
        # Get next page url
        next_page_url = response.xpath('//a[@class="next"]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_cok_satanlar)
        # If there is no next page, yield the category
        else:
            products_item = KitapYurduProducts(
                category_title=category_title, cok_satanlar=self.cok_satanlar
            )
            yield products_item

    def parse_yeni_cikanlar(self, response):
        """Parse yeni_cikanlar page and yield next page if exists"""
        products = response.xpath('//div[contains(@class, "product-cr")]')
        category_title = response.xpath('//div[@id="content"]/h1/text()').get()

        for product in products:
            book_name = product.xpath(
                './/div[@class="name ellipsis"]/a/span/text()'
            ).get()

            publisher = product.xpath(
                './/div[@class="publisher"]//span/a/span/text()'
            ).get()
            price = product.xpath(
                './/div[@class="price"]//div[@class="price-new "]/span[@class="value"]/text()'
            ).get()

            author_selector = product.xpath('.//div[@class="author"]//span/a/text()')
            authors = author_selector.extract()
            combined_authors = (
                " ".join(authors).strip()
                or product.xpath(
                    './/div[@class="author compact ellipsis"]/a/text()'
                ).get()
            )
            # Convert price to float
            if price:
                price = price.replace(".", "").replace(",", ".").strip()
                book_price = float(price)
            else:
                book_price = None
            # Create a dictionary for each book
            self.yeni_cikanlar.append(
                KitapYurduBooks(
                    book_name=book_name,
                    book_publisher=publisher,
                    book_author=combined_authors,
                    book_price=book_price,
                )
            )
        # Get next page url
        next_page_url = response.xpath('//a[@class="next"]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_yeni_cikanlar)
        # If there is no next page, yield the category
        else:
            products_item = KitapYurduProducts(
                category_title=category_title, yeni_cikanlar=self.yeni_cikanlar
            )
            yield products_item

    def parse(self, response):
        """Parse main page and yield category page"""
        categories = response.xpath('//div[@class="category-container"]/div')
        for category in categories:
            for response in category.xpath(
                '//div[@class="category"]/a[@class="category-item"]'
            ):
                self.category_link = response.xpath("@href").get()

                yield scrapy.Request(
                    url=self.category_link, callback=self.parse_category
                )
