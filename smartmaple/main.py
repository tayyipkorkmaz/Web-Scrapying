from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from smartmaple.spiders.kitapsepeti import KitapsepetiSpider
from smartmaple.spiders.kitapyurdu import KitapyurduSpider
from scrapy.utils.log import configure_logging


def main():
    """Run spiders"""

    configure_logging()
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(KitapyurduSpider)
    process.crawl(KitapsepetiSpider)

    process.start()


if __name__ == "__main__":
    main()
