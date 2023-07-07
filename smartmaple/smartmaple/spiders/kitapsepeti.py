import scrapy
from smartmaple.items import KitapSepetiBooks, KitapSepetiProducts


class KitapsepetiSpider(scrapy.Spider):
    name = "kitapsepeti"
    allowed_domains = ["www.kitapsepeti.com"]
    start_urls = ["https://www.kitapsepeti.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "smartmaple.pipelines.KitapsepetiPipeline": 300,
        }
    }

    def parse_category(self, response):
        """Parse category page and yield next page if exists"""
        category_name = response.xpath("//title/text()").get().split(" |")[0]
        kitaplar = []
        # Get books
        for product in response.css(
            "div.fl.col-12.catalogWrapper div.col-3.col-md-4.col-sm-6.col-xs-6.p-right.mb.productItem.zoom.ease"
        ):
            name = (
                product.css(
                    "div.box.col-12.text-center a.text-description.detailLink::text"
                )
                .get()
                .strip()
            )
            publisher = product.css(
                "div.box.col-12.text-center a.text-title.mt::text"
            ).get()
            author = product.css(
                "div.box.col-12.text-center a.text-title:not(.mt)::text"
            ).get()
            price = (
                product.xpath(".//div[contains(@class, 'currentPrice')]/text()")
                .get()
                .strip()
            )
            # Convert price to float
            if price:
                price = price.strip().replace("\nTL", "")
                price = price.replace(".", "").replace(",", ".")
                book_price = float(price)

            # Create book item
            kitaplar.append(
                KitapSepetiBooks(
                    book_name=name,
                    publisher_name=publisher,
                    book_author=author,
                    book_price=book_price,
                )
            )
        # Get next page if exists
        next_page = response.xpath(
            '//div[@class="fn d-inline-block col-sm-12 text-center productPager"]/a[@class="next"]/@href'
        ).get()

        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse_category)
        # Yield category item
        else:
            product_item = KitapSepetiProducts(
                category_name=category_name, books=kitaplar
            )
            yield product_item

    def parse(self, response):
        """Parse main page and yield category pages"""
        self.header_link = "https://www.kitapsepeti.com"
        categories = response.xpath(
            "//div[@id='footerMiddle']//a[contains(@href, '/edebiyat') or contains(@href, '/cocuk-kitaplari') or contains(@href, '/tarih-kitaplari') or contains(@href, '/saglik') or contains(@href, '/yemek-kitaplari')]"
        )
        for category in categories:
            category_link = category.xpath(".//@href").extract_first()
            yield scrapy.Request(
                url=self.header_link + category_link, callback=self.parse_category
            )
