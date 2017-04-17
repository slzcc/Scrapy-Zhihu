# Scrapy 爬虫登入 `知乎网` 使用 `API` 爬取用户信息
这里的爬虫已经结合 Docker , 由于没有使用多线程工作所以这里使用 Docker 启动特定数量的服务进行爬数据, 镜像拉去地址:
```
$ docker pull registry.aliyuncs.com/slzcc/scrapy_zhihu:latest
```
项目内有 `Dockerfile` 提供参考。

用到的服务列表:
 *  Mongo
 *  Redis

Redis 使用 Lists 队列保存需要爬取的 URL，这里是爬虫自己添加 URL 队列, 队列名称为 `zhihu:start_urls`。
Mongo 会保存 Cookie 信息，和最终爬取的用户信息, 使用的库名为 `scrapy_session`, `zhihu`。

原理是需要使用用户的 Cookie 进行爬虫的登入授权，其中需要使用一台拥有图形化系统的服务器进行激活码手动填写，执行:
```
$ docker run --rm -it -v ${PWD}/code:/Scrapy-Zhihu/code --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:latest python rediszhihu/login.py
```
执行上述命令后会让你填写用户，密码，验证码，验证码需要手动查看 `~/code/code.gif` 图片内容进行填写。
如果成功登入会把 Cookie 保存到本地的 Mongo 的 scrapy_session 库里面, 如果本地没有 Mongo 请修改下面的环境变量进行修改, 这里默认会让你输入两次账号密码同一个账号也是没问题的。
>建议: 登入的 Cookie 可以设置多个，如果想避免被屏蔽，这里建议使用不同的账号获取 Cookie，这里没有试验 Cookie 数量的上限值, 不做概述。

拿到 Cookie 后需要设置 Mongo 与 Redis 的服务器地址与端口, 默认`localhost`, 可自定义环境变量:
```
REDIS_DB_HOST=127.0.0.1
REDIS_DB_PORT=6379
MONGODB_DB_HOST=127.0.0.1
MONGODB_DB_PORT=27017
MONGODB_DB_DBNAME=zhihu
MONGODB_DB_DOCNAME=user_information
``` 
爬虫启动:
```
$ docker run -d --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:latest
```
请自行修改环境变量适合自己的环境执行爬虫的启动, 测试开启数十个容器进行爬取数据无任何问题。

可以使用 `Swarm` 集群模式启动 10 数量的服务:
```
$ docker service create --name scrapy_zhihu -e MONGODB_DB_HOST=127.0.0.1 -e REDIS_DB_HOST=127.0.0.1 --replicas 10 registry.aliyuncs.com/slzcc/scrapy_zhihu:latest
```

因为默认爬虫是会在 Redis 队列获取 URL 进行爬取的，所以需要手动填入 URL 进行爬虫的激活，进入 Rdis 后执行:
```
lrange zhihu:start_urls 0 -1
lpush zhihu:start_urls https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30
```
第一条命令是创建 `zhihu:start_urls` 队列，第二条是 URL 地址。

友情提示: 每个容器会占用 40MB+ 内存大小，请根据自己需求开启容器的数量。

## 验证 Cookie 是否失效
验证 Cookie 也是使用简单的多少时间内进行一次验证，使用 Mongo 里面的 Cookie 列表进行逐一请求进行排查，可以设置 `TimeCounter` 变量设置时间，默认时间为 `60秒`，单位是 `秒`，执行命令:
```
$ docker run -d --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:latest python rediszhihu/remove_abandoned_cookie.py
```
如果 Cookie 没问题会打印，如果有问题会先打印出有问题的 Cookie 并删除，容器执行完会自动退出，这里需要配合集群进行启动从而保证 Cookie 验证容器持续存。

## 中间件说明
爬虫使用了 `Middleware` 中间件进行用户的 Cookie 、User-Agent 的动态变更，并且已对 Proxy 进行了配置，如果需要请打开 `settings.py` 的 `rediszhihu.middlewares.ProxyMiddleware` 注释。并
定义 `settings.py` 里面的 `IP_LIST` 列表这是使用代理的 IP 池，默认填写了一个。

## 爬取用户信息数量查询
查看已经爬取用户信息的数量，可以使用内置已经写好的方法进行查询:
```
$ docker run --rm -i --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:latest python rediszhihu/number_queries.py
```

队列展示图:
![Redis Lists up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-mongo/template/redis.png)
数据展示图:
![Mongo lists up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-mongo/template/mongo01.png)
![Mongo user_info up](https://github.com/slzcc/Scrapy-Zhihu/blob/docker-mongo/template/mongo02.png)

