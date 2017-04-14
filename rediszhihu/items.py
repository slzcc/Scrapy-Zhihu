# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RediszhihuItem(scrapy.Item):
    info_list = scrapy.Field()
    followers_list = scrapy.Field()
    token = scrapy.Field()
