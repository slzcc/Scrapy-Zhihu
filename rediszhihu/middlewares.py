# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.conf import settings
from scrapy import signals
import random
import requests
import json
import os

class RediszhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UAMiddleware(object):
    user_agent_list = settings['USER_AGENT_LIST']

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = ua


class ProxyMiddleware(object):
    ip_list = settings['IP_LIST']

    def process_request(self, request, spider):
        ip = random.choice(self.ip_list)
        request.meta['proxy'] = ip

SystemEnv = {

    'ELASTICSEARCH_DB_SERVER': os.getenv('ELASTICSEARCH_DB_SERVER'),
    'ELASTICSEARCH_COOKIE_INDEX': os.getenv('ELASTICSEARCH_COOKIE_INDEX'),
    'ELASTICSEARCH_COOKIE_TYPE': os.getenv('ELASTICSEARCH_COOKIE_TYPE'),
    'ELASTICSEARCH_DATA_INDEX': os.getenv('ELASTICSEARCH_DATA_INDEX'),
    'ELASTICSEARCH_DATA_TYPE': os.getenv('ELASTICSEARCH_DATA_TYPE'),
    'REDIS_HOST': os.getenv('REDIS_DB_HOST'),
    'QUERY_ACCOUNT_NUMBER': os.getenv('QUERY_ACCOUNT_NUMBER'),
    'QUERY_DATA_NUMBER': os.getenv('QUERY_DATA_NUMBER'),
    'TimeCounter': os.getenv('TimeCounter'),
    'REDIS_PORT': os.getenv('REDIS_DB_PORT')

}

cookie_list = []
Cookie_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'], SystemEnv['ELASTICSEARCH_COOKIE_INDEX'], SystemEnv['ELASTICSEARCH_COOKIE_TYPE'], int(SystemEnv['QUERY_ACCOUNT_NUMBER']))

es_list = requests.get(Cookie_urls)
data = json.loads(es_list.text)

for i in data['hits']['hits']:
    _id = i['_id']
    i['_source'].pop('@timestamp')
    cookie_list.append(i['_source'])


class CookieMiddleware(object):

    def process_request(self, request, spider):

        cookie = random.choice(cookie_list)
        request.cookies = cookie