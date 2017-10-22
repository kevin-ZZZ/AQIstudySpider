# coding:utf-8

import scrapy
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from scrapy.linkextractors import LinkExtractor
from AQI.items import AqiItem


class AqiCrawlSpider(RedisCrawlSpider):

    name = "aqi_crawlspider"
    allowed_domains = ["aqistudy.cn"]

    redis_key = "aqi_crawlspider"

    rules = (
        # 不指定回调函数，框架默认指示 follow = True
        Rule(LinkExtractor(allow=r"monthdata\.php\?city=")),
        # 指定回调函数，框架默认指示 follow = False
        Rule(LinkExtractor(allow=r"daydata\.php\?city="), callback = "parse_item")
    )


    def parse_item(self, response):
        node_list = response.xpath("//tr")
        node_list.pop(0)

        city_name = response.xpath("//h3[@id='title']/text()").extract_first()

        for node in node_list:
            item = AqiItem()
            item['city'] = city_name[8:-11]
            item['date'] = node.xpath("./td[1]/text()").extract()[0]
            item['aqi'] = node.xpath("./td[2]/text()").extract()[0]
            item['level'] = node.xpath("./td[3]/span/text()").extract()[0]
            item['pm2_5'] = node.xpath("./td[4]/text()").extract()[0]
            item['pm10'] = node.xpath("./td[5]/text()").extract()[0]
            item['so2'] = node.xpath("./td[6]/text()").extract()[0]
            item['co'] = node.xpath("./td[7]/text()").extract()[0]
            item['no2'] = node.xpath("./td[8]/text()").extract()[0]
            item['o3'] = node.xpath("./td[9]/text()").extract()[0]

            yield item
