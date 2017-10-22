# -*- coding:utf-8 -*-

import scrapy

from scrapy_redis.spiders import RedisSpider
from AQI.items import AqiItem



class AqiSpider(RedisSpider):
    name = "aqi_spider"
    allowed_domains = ["aqistudy.cn"]

    base_url = "https://www.aqistudy.cn/historydata/"
    redis_key = "aqispider:start_urls"

    def parse(self, response):
        '''
            从html文档流中提取出节点
        '''
        city_link_list = response.xpath("//div[@class='all']//li/a/@href").extract()
        city_name_list = response.xpath("//div[@class='all']//li/a/text()").extract()

        for city_link, city_name in zip(city_link_list, city_name_list):
            yield scrapy.Request(self.base_url + city_link, meta = {"city_name" : city_name}, callback = self.parse_month)


    def parse_month(self, response):
        '''
            解析返回的月数据列表页的数据，并且将数据进一步交由self.parse_day解析
        '''
        month_link_list = response.xpath("//td[@align='center']//a/@href").extract()
        for month_link in month_link_list:
            yield scrapy.Request(self.base_url + month_link, meta = response.meta, callback = self.parse_day)


    def parse_day(self, response):
        '''
            解析返回的响应，从中获取每一天数据，分别从里面提取出要的数据
        '''
        node_list = response.xpath("//tr")
        node_list.pop(0)

        for node in node_list:
            item = AqiItem()
            item['city'] = response.meta["city_name"]
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
