from pymongo import MongoClient
import requests
import json
import time
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

urls= 'https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30'

MONGODB_HOST = os.getenv('MONGODB_DB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_DB_PORT'))
TimeCounter = int(os.getenv('Time'))

conn = MongoClient(MONGODB_HOST, MONGODB_PORT)

db = conn.scrapy_session

cookie_list = []

for item in db.cookie.find():
    Cookie_id = item.pop('_id')
    time.sleep(TimeCounter)
    source = requests.get(urls, headers=header, cookies=item).content
    source = json.loads(source)['paging']['is_start']
    if source == True:
        print('By verifying the Cookie: ', item)
    else:
        print('Delete the Cookie: ', item)
        db.cookie.remove({'_id': Cookie_id})