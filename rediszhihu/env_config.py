# -*- coding: utf-8 -*-
import os

SystemEnv = {

    'ELASTICSEARCH_DB_SERVER': os.getenv('ELASTICSEARCH_DB_SERVER'),
    'ELASTICSEARCH_COOKIE_INDEX': os.getenv('ELASTICSEARCH_COOKIE_INDEX'),
    'ELASTICSEARCH_COOKIE_TYPE': os.getenv('ELASTICSEARCH_COOKIE_TYPE'),
    'ELASTICSEARCH_DATA_INDEX': os.getenv('ELASTICSEARCH_DATA_INDEX'),
    'ELASTICSEARCH_DATA_TYPE': os.getenv('ELASTICSEARCH_DATA_TYPE'),
    'QUERY_ACCOUNT_NUMBER': int(os.getenv('QUERY_ACCOUNT_NUMBER')),
    'QUERY_DATA_NUMBER': int(os.getenv('QUERY_DATA_NUMBER')),
    'TimeCounter': int(os.getenv('TimeCounter')),
    'REDIS_HOST': os.getenv('REDIS_HOST'),
    'REDIS_PORT': int(os.getenv('REDIS_PORT'))

}