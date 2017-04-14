# 知乎 API 爬虫
进入项目后直接执行 main.py 即可,需要在本地准备 Redis 和 Mongo 服务，默认会读取 localhost 地址，端口都是默认如果需要修改请更改 sttings.py 内的参数。
登入成功后会从 Redis lists 里面获取 url 地址进行爬取，这时候手动执行:
```
lpush zhihu:start_urls https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30
```
把一条 url 放置在队列内激活爬虫服务，之后会自行获取过滤 url 存到队列内部。

如果队列不存在请执行：
```
lrange zhihu:start_urls 0 -1
```
