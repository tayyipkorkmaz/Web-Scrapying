# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class KitapyurduPipeline:
    """MongoDB pipeline for storing scraped items"""

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create your spiders."""
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE")
        collection_name = crawler.settings.get("KITAPYURDU_COLLECTION")
        return cls(mongo_uri, mongo_db, collection_name)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        """This method is called when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """This method is called for every item pipeline component."""
        self.collection.insert_one(dict(item))
        return item


class KitapsepetiPipeline:
    """MongoDB pipeline for storing scraped items"""

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create your spiders."""
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE")
        collection_name = crawler.settings.get("KITAPSEPETI_COLLECTION")
        return cls(mongo_uri, mongo_db, collection_name)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        """This method is called when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """This method is called for every item pipeline component."""
        self.collection.insert_one(dict(item))
        return item
