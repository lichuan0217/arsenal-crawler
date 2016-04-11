# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import ArsenalCardItem, ArsenalArticalItem


class ArsenalPipeline(object):

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_collection_item, mongo_collection_artical):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_collection_item = mongo_collection_item
        self.mongo_collection_artical = mongo_collection_artical

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get("MONGODB_SERVER"),
            mongo_port=crawler.settings.get("MONGODB_PORT"),
            mongo_db=crawler.settings.get("MONGODB_DB"),
            mongo_collection_item=crawler.settings.get(
                "MONGODB_COLLECTION_ITEM"),
            mongo_collection_artical=crawler.settings.get(
                "MONGODB_COLLECTION_ARTICAL")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_server, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection_item = self.db[self.mongo_collection_item]
        self.collection_artical = self.db[self.mongo_collection_artical]
        self.latest_item = self.collection_item.find().sort("artical_id", pymongo.DESCENDING)[0]
        self.latest_artical_id = self.latest_item['artical_id']
        print self.latest_item
        print self.latest_artical_id

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
    	print "process_item"
    	if item["artical_id"] <= self.latest_artical_id:
    		spider.close_down = True
    		return item
        if isinstance(item, ArsenalCardItem):
            print "ArsenalCardItem!!!"
            self.collection_item.insert(dict(item))
        if isinstance(item, ArsenalArticalItem):
            print "ArsenalArticalItem!!!"
            self.collection_artical.insert(dict(item))
        return item
