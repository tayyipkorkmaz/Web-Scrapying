# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KitapSepetiBooks(scrapy.Item):
    """KitapSepetiBooks class for KitapSepetiBooks items"""
    book_name = scrapy.Field()
    publisher_name = scrapy.Field()
    book_author = scrapy.Field()
    book_price = scrapy.Field()


class KitapSepetiProducts(scrapy.Item):
    """KitapSepetiProducts class for KitapSepetiProducts items"""
    category_name = scrapy.Field()
    books = scrapy.Field()


class KitapYurduBooks(scrapy.Item):
    """KitapYurduBooks class for KitapYurduBooks items"""
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_price = scrapy.Field()
    book_publisher = scrapy.Field()


class KitapYurduProducts(scrapy.Item):
    """KitapYurduProducts class for KitapYurduProducts items"""
    category_title = scrapy.Field()
    cok_satanlar = scrapy.Field()
    yeni_cikanlar = scrapy.Field()
