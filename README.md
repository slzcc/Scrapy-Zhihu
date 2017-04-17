# Scrapy 爬取 知乎网 用户信息并使用 Docker 进行爬取数据

用到的服务列表:
  Mongo
  Redis

Redis 使用 Lists 队列保存需要爬取的 URL，这里是爬虫自己回去添加列表, 队列名称为 `zhihu:start_urls`。
Mongo 会保存 Cookie 信息，和最终爬取的用户信息, 使用的库名为 `scrapy_session`, `zhihu`。

原理是需要使用用户的 Cookie 进行爬虫的登入授权，其中需要使用一台拥有图形化系统的服务器进行激活码手动填写，执行:
```
$ docker run --rm -it -v ${PWD}/code:/Scrapy-Zhihu/code --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:0.4.1 python rediszhihu/login.py
```
执行上述命令后会让你填写用户，密码，验证码，如果成功登入会把 cookie 保存到 Mongo 的 scrapy_session 库里面。
登入的 cookie 可以设置多个，这里建议使用不同的账号获取 Cookie，这里没有试验 Cookie 数量的上限值。

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
$ docker run -d --net host registry.aliyuncs.com/slzcc/scrapy_zhihu:0.3.1
```
请自行修改环境变量适合自己的环境执行爬虫的启动。
