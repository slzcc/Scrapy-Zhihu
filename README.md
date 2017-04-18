# Scrapy 爬虫登入 `知乎网` 使用 `API` 爬取用户信息
在使用此项目时请先了解 Scrapy 项目源码如何实现的:
```
$ git clone -b docker-elasticsearch https://github.com/slzcc/Scrapy-Zhihu.git
```

这里的爬虫已经结合 Docker , 由于没有使用多线程工作所以这里使用 Docker 启动特定数量的服务进行爬数据, 镜像拉去地址:
```
$ docker pull registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch
```

项目内有 `Dockerfile` 提供参考。

用到的服务列表:
 *  Elasticsearch
 *  Redis

Redis 使用 Lists 队列保存需要爬取的 URL，这里是爬虫自己添加 URL 队列, 队列名称为 `zhihu:start_urls`。
Elasticsearch 会保存 Cookie 信息，和最终爬取的用户信息, 使用的 `index` 名为 `scrapy-zhihu`, type 为 `item`。

## 注册 Cookie
原理是需要使用用户的 Cookie 进行爬虫的登入授权，其中需要使用一台拥有图形化系统的服务器进行激活码手动填写，执行:
```
$ docker run -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 --rm -it -v ${PWD}/code:/Scrapy-Zhihu/code --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch python rediszhihu/login.py
```
>注意: 请结合下列的环境变量说明修改自己所需的环境。

执行上述命令后会让你填写用户，密码，验证码，验证码需要手动查看 `~/code/code.gif` 图片内容进行填写。
如果成功登入会把 Cookie 保存到本地的 Elasticsearch 的 `scrapy-cookie` 的 `item` type 里面, 如果本地没有 Elasticsearch 服务请修改下面的环境变量进行修改, 这里默认会让你输入两次账号密码同一个账号也是没问题的。

>建议: 登入的 Cookie 可以设置多个，如果想避免被屏蔽，这里建议使用不同的账号获取 Cookie，这里没有试验 Cookie 数量的上限值, 不做概述。

## 环境变量说明
拿到 Cookie 后需要设置 Elasticsearch 与 Redis 的服务器地址与端口, 默认`localhost`, 可自定义环境变量:
Redis 服务的服务地址与端口:
```
REDIS_DB_HOST=127.0.0.1
REDIS_DB_PORT=6379
```
Elasticsearch 服务地址, 还可以设置变更上传的 `index` ,以及 Cookie 保存的 `index`, 并支持变更 `type`。
```
ELASTICSEARCH_DB_SERVER=http://localhost:9200
ELASTICSEARCH_COOKIE_INDEX=scrapy-cookie
ELASTICSEARCH_COOKIE_TYPE=item
ELASTICSEARCH_DATA_INDEX=scrapy-zhihu
ELASTICSEARCH_DATA_TYPE=item
```
后续查询所需的环境变量, 其中 `QUERY_ACCOUNT_NUMBER` 是执行 `rediszhihu/number_queries.py` 查询 Cookie 的最大查询数量，`QUERY_DATA_NUMBER` 是执行 `rediszhihu/number_queries.py` 查询数据最大显示数量，`TimeCounter` 是执行 `rediszhihu/remove_abandoned_cookie.py` 后检测每次 Cookie 验证的时间，单位是`秒`。
```
QUERY_ACCOUNT_NUMBER=100
QUERY_DATA_NUMBER=5
TimeCounter=60
```


## 启动
爬虫启动:
```
$ docker run -d --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch
```
请自行修改环境变量适合自己的环境执行爬虫的启动, 测试开启数十个容器进行爬取数据无任何问题。

可以使用 `Swarm` 集群模式启动 10 数量的服务:
```
$ docker service create --name scrapy_zhihu -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 -e REDIS_DB_HOST=127.0.0.1 --replicas 10 registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch
```

因为默认爬虫是会在 Redis 队列获取 URL 进行爬取的，所以需要手动填入 URL 进行爬虫的激活，进入 Redis 后执行:
```
lrange zhihu:start_urls 0 -1
lpush zhihu:start_urls https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30
```
第一条命令是创建 `zhihu:start_urls` 队列，第二条是 URL 地址。

友情提示: 每个容器会占用 40MB+ 内存大小，请根据自己需求开启容器的数量。

## 验证 Cookie 是否失效
验证 Cookie 也是使用简单的多少时间内进行一次验证，使用 Mongo 里面的 Cookie 列表进行逐一请求进行排查，可以设置 `TimeCounter` 变量设置时间，默认时间为 `60秒`，单位是 `秒`，执行命令:
```
$ docker run -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 -d --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch python rediszhihu/remove_abandoned_cookie.py
```
如果 Cookie 没问题会打印，如果有问题会先打印出有问题的 Cookie 并删除，容器执行完会自动退出，这里需要配合集群进行启动从而保证 Cookie 验证容器持续进行检测。

## 中间件说明
爬虫使用了 `Middleware` 中间件进行用户的 Cookie 、User-Agent 的动态变更，并且已对 Proxy 进行了配置，如果需要请打开 `settings.py` 的 `rediszhihu.middlewares.ProxyMiddleware` 注释。并
定义 `settings.py` 里面的 `IP_LIST` 列表这是使用代理的 IP 池，默认填写了一个。

## 爬取用户信息数量查询
查看已经爬取用户信息的数量,信息内容,Cookie 列表,可以使用内置已经写好的方法进行查询:
```
$ docker run -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 --rm -it --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:elasticsearch python rediszhihu/number_queries.py
```
执行后会进入交互模式，请更换对应的环境编辑进行检测，输入的命令说明:
  * data 为直接查看数据。
  * num 为查看爬取数据总数。
  * cookie 查看 cookie 列表。

## 展示图
### 队列展示图
列出队列等待被消费的 `URL`
![Redis Lists up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/redis01.png)
### 数据展示图
元数据信息
![Elasticsearch 01 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch01.png)
索引信息
![Elasticsearch 02 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch02.png)
性别饼图
![Elasticsearch 03 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch03.png)
粉丝名次柱状图
![Elasticsearch 04 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch04.png)
行业分布柱状图
![Elasticsearch 05 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch05.png)
职业分布柱状图
![Elasticsearch 06 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch06.png)
人数数量柱状图
![Elasticsearch 07 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch07.png)
员工数量柱状图
![Elasticsearch 08 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch08.png)
校友数量柱状图
![Elasticsearch 09 Data up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-elasticsearch/template/elasticsearch09.png)
