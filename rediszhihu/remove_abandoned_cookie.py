import requests
import json
import time
from elasticsearch import Elasticsearch
from .env_config import SystemEnv

header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

Cookie_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'], SystemEnv['ELASTICSEARCH_COOKIE_INDEX'], SystemEnv['ELASTICSEARCH_COOKIE_TYPE'], SystemEnv['QUERY_ACCOUNT_NUMBER'])

es = Elasticsearch([SystemEnv['ELASTICSEARCH_DB_SERVER]']])

Validation_urls= 'https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30'

es_list = requests.get(Cookie_urls)
data = json.loads(es_list.text)
for i in data['hits']['hits']:
    _id = i['_id']
    i['_source'].pop('@timestamp')
    cookie = i['_source']
    time.sleep(SystemEnv['TimeCounter'])
    source = requests.get(Validation_urls, headers=header, cookies=cookie).content
    source = json.loads(source)['paging']['is_start']
    if source == True:
        print('By verifying the Cookie: ', cookie)
    else:
        print('Delete the Cookie: {}, ID is: {}'.format(cookie, _id), )
        es.delete(index=SystemEnv['ELASTICSEARCH_COOKIE_INDEX'], doc_type=SystemEnv['ELASTICSEARCH_COOKIE_TYPE'], id=_id)


