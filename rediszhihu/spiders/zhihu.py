# -*- coding: utf-8 -*-
import scrapy
import time
import os
import json
import math
import redis
from scrapy_redis.spiders import RedisSpider
from rediszhihu.items import RediszhihuItem
from rediszhihu.myconfig import UsersConfig

class ZhihuSpider(RedisSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    # start_urls = ['https://www.zhihu.com/#signin']
    Counter = 0
    redis_key = 'zhihu:start_urls'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

    login_url = 'https://www.zhihu.com/login/email'
    url = 'https://www.zhihu.com/api/v4/members/stone-cok?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics',

    redis_q = redis.StrictRedis(connection_pool=redis.ConnectionPool(host='127.0.0.1', port=6379, db=0))

    def parse(self, response):
        global _xsrf

        if self.Counter == 0:
            _xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
            # 获取验证码地址
            captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(math.ceil(time.time() * 1000)) + '&type=login&lang=cn'
            # 准备下载验证码
            yield scrapy.Request(
                url=captcha_url,
                headers=self.headers,
                meta={
                    # 'proxy': self.proxy,
                    'cookiejar': 0,
                    '_xsrf': _xsrf
                },
                callback=self.download_captcha
            )
        else:
            return self.token_start()
            # source = RediszhihuItem()
            # source['followers_list'] = json.loads(response.body_as_unicode())
            # for i, j in enumerate(source['followers_list']):
            #     user_token = source['followers_list']['data'][i]['url_token']
            #     user_followers_apt = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30'.format(
            #         user_token)
            #     user_info_apt = 'https://www.zhihu.com/api/v4/members/{}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'.format(
            #         user_token)
            #     self.redis_q.lpush('zhihu:start_urls', user_followers_apt)
            #     yield scrapy.Request(
            #         url=user_info_apt,
            #         headers=self.headers,
            #         meta={
            #             # 'proxy': UsersConfig['proxy'],
            #             'cookiejar': response.meta['cookiejar'],
            #             'from': {
            #                 'sign': 'else',
            #                 'data': {}
            #             }
            #         },
            #         callback=self.user_start,
            #         dont_filter=True
            #     )


    def download_captcha(self, response):
        # 下载验证码
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        # 用软件打开验证码图片
        os.system('open captcha.gif')
        # 输入验证码
        print('Please enter captcha: ')
        captcha = input().strip()
        print(captcha)
        print(type(captcha))
        global _xsrf
        print(_xsrf)
        print(UsersConfig['email'])
        print(UsersConfig['password'])
        print(response.meta)
        yield scrapy.FormRequest(
            url=self.login_url,
            headers=self.headers,
            formdata={
                'email': UsersConfig['email'],
                'password': UsersConfig['password'],
                '_xsrf': _xsrf,
                'remember_me': 'true',
                'captcha': captcha,
                'captcha_type': 'cn'
            },
            meta={
                # 'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar']
            },
            callback=self.request_zhihu
        )
    def request_zhihu(self, response):
        with open('/Users/shilei/Json/zhihu-login-error.json', 'wb') as fp:
            fp.write(response.body)
        print(response.body.decode())
        print(self.url)
        # if response.body.errcode:
        #     self.redis_q.lpush('zhihu:start_urls', 'https://www.zhihu.com/#signin')
        #     self.Counter = 0
        #     return
        yield scrapy.Request(
            url='https://www.zhihu.com/api/v4/members/stone-cok/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30',
            # url = 'https://www.zhihu.com/api/v4/members/stone-cok?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics',
            headers=self.headers,
            meta={
                # 'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar'],
                'from': {
                    'sign': 'else',
                    'data': {}
                }
            },
            callback=self.token_start,
            dont_filter=True
        )

    def token_start(self, response):
        source = RediszhihuItem()
        source['followers_list'] = json.loads(response.body_as_unicode())
        for i, j in enumerate(source['followers_list']):
            user_token = source['followers_list']['data'][i]['url_token']
            user_followers_apt = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30'.format(user_token)
            user_info_apt = 'https://www.zhihu.com/api/v4/members/{}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'.format(user_token)
            self.redis_q.lpush('zhihu:start_urls', user_followers_apt)
            yield scrapy.Request(
                url=user_info_apt,
                headers=self.headers,
                meta={
                    # 'proxy': UsersConfig['proxy'],
                    'cookiejar': response.meta['cookiejar'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback=self.user_start,
                dont_filter=True
            )


    def user_start(self, response):
        source = RediszhihuItem()
        source['info_list'] = json.loads(response.body_as_unicode())
        source['token'] = source['info_list']['url_token']
        # print(source)
        # print(source['info_list']['url_token'])
        print('token', source['token'])
        self.Counter += 1
        yield source
