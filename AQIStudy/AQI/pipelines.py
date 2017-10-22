# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import CsvItemExporter

from datetime import datetime
import pymongo
import redis
import json
import csv


class AqiPipeline(object):
    def process_item(self, item, spider):
        item['utc_time'] = datetime.utcnow()
        item['source'] = spider.name
        return item

# 保存到csv文件
class AqiCsvPipeline(object):
    def open_spider(self, spider):
        # 创建csv文件对象
        self.f = open("aqi.csv", "w")
        #创建csv文件读写对象
        self.csv_exporter = CsvItemExporter(self.f)
        # 开始执行item数据的读写操作
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 停止item数据的读写操作
        self.csv_exporter.finish_exporting()
        self.f.close()

# 保存到redis数据库
class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.redis_client = redis.Redis(host="127.0.0.1", port=6379)
        #self.redis_client = redis.StrickRedis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        content = json.dumps(dict(item))
        self.redis_client.lpush("aqi_item", content)
        return item
        
# 保存到mongo数据库
class AqiMongoPipeline(object):
    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db_name = self.mongo_client["AQI"]
        self.sheet_name = self.db_name["aqi_item"]

    def process_item(self, item, spider):
        self.sheet_name.insert(dict(item))
        return item













