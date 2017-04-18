import json
import requests
import os

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

while True:
    print("English：Incoming, please you need to get the information and data content data, data total number 'num, Cookie sheet' cookies'.")
    print("Chinese：请传入你需要获取的信息有、数据内容 ’data’, 数据总数量 ‘num’，Cookie 表 ‘cookie’。")

    Pass = input("Passing parameters you need: ")

    if Pass == 'data':
        Data_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                        SystemEnv['ELASTICSEARCH_DATA_INDEX'],
                                                        SystemEnv['ELASTICSEARCH_DATA_TYPE'],
                                                        int(SystemEnv['QUERY_DATA_NUMBER']))
        es_list = requests.get(Data_urls)
        data = json.loads(es_list.text)
        print('<--------------------------------------------------------------------------------------------------------------------------------------*')
        print(data)
        print('*-------------------------------------------------------------------------------------------------------------------------------------->\n')

    elif Pass == 'num':
        Data_urls = "{}/{}/{}/_search".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                        SystemEnv['ELASTICSEARCH_DATA_INDEX'],
                                                        SystemEnv['ELASTICSEARCH_DATA_TYPE']
                                                        )
        es_list = requests.get(Data_urls)
        data = json.loads(es_list.text)
        print('<--------------------------------------------------------------------------------------------------------------------------------------*')
        print('Information for a total of: ', data['hits']['total'] + 'article')
        print('*-------------------------------------------------------------------------------------------------------------------------------------->\n')

    elif Pass == 'cookie':
        Cookie_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                      SystemEnv['ELASTICSEARCH_COOKIE_INDEX'],
                                                      SystemEnv['ELASTICSEARCH_COOKIE_TYPE'],
                                                      int(SystemEnv['QUERY_ACCOUNT_NUMBER']))
        es_list = requests.get(Cookie_urls)
        data = json.loads(es_list.text)
        data = json.loads(es_list.text)
        for i in data['hits']['hits']:
            _id = i['_id']
            print('Cookie List: ')
            print('<--------------------------------------------------------------------------------------------------------------------------------------*')
            print('The Cookie Data ID: {}\n\nContent is: \n{}\n'.format(_id, i['_source']))
            print('*-------------------------------------------------------------------------------------------------------------------------------------->\n')