import requests
import json
import time
from elasticsearch import Elasticsearch
import os

header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

SystemEnv = {

    'ELASTICSEARCH_DB_SERVER': os.getenv('ELASTICSEARCH_DB_SERVER'),
    'ELASTICSEARCH_COOKIE_INDEX': os.getenv('ELASTICSEARCH_COOKIE_INDEX'),
    'ELASTICSEARCH_COOKIE_TYPE': os.getenv('ELASTICSEARCH_COOKIE_TYPE'),
    'ELASTICSEARCH_DATA_INDEX': os.getenv('ELASTICSEARCH_DATA_INDEX'),
    'ELASTICSEARCH_DATA_TYPE': os.getenv('ELASTICSEARCH_DATA_TYPE'),
    'REDIS_HOST': os.getenv('REDIS_HOST'),
    'QUERY_ACCOUNT_NUMBER': os.getenv('QUERY_ACCOUNT_NUMBER'),
    'QUERY_DATA_NUMBER': os.getenv('QUERY_DATA_NUMBER'),
    'TimeCounter': os.getenv('TimeCounter'),
    'REDIS_PORT': os.getenv('REDIS_PORT')

}

Cookie_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'], SystemEnv['ELASTICSEARCH_COOKIE_INDEX'], SystemEnv['ELASTICSEARCH_COOKIE_TYPE'], int(SystemEnv['QUERY_ACCOUNT_NUMBER']))

es = Elasticsearch([SystemEnv['ELASTICSEARCH_DB_SERVER]']])

Validation_urls= 'https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30'

es_list = requests.get(Cookie_urls)
data = json.loads(es_list.text)
for i in data['hits']['hits']:
    _id = i['_id']
    i['_source'].pop('@timestamp')
    cookie = i['_source']
    time.sleep(int(SystemEnv['TimeCounter']))
    source = requests.get(Validation_urls, headers=header, cookies=cookie).content
    source = json.loads(source)['paging']['is_start']
    if source == True:
        print('By verifying the Cookie: ', cookie)
    else:
        print('Delete the Cookie: {}, ID is: {}'.format(cookie, _id), )
        es.delete(index=SystemEnv['ELASTICSEARCH_COOKIE_INDEX'], doc_type=SystemEnv['ELASTICSEARCH_COOKIE_TYPE'], id=_id)


