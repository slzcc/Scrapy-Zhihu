from .env_config import SystemEnv
import json
import requests

while True:
    print("English：Incoming, please you need to get the information and data content data, data total number 'num, Cookie sheet' cookies'.")
    print("Chinese：请传入你需要获取的信息有、数据内容 ’data’, 数据总数量 ‘num’，Cookie 表 ‘cookie’。")

    Pass = input("Passing parameters you need: ")

    if Pass == 'data':
        Data_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                        SystemEnv['ELASTICSEARCH_DATA_INDEX'],
                                                        SystemEnv['ELASTICSEARCH_DATA_TYPE'],
                                                        SystemEnv['QUERY_DATA_NUMBER'])
        es_list = requests.get(Data_urls)
        data = json.loads(es_list.text)
        print(data)
    elif Pass == 'num':
        Data_urls = "{}/{}/{}/_search".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                        SystemEnv['ELASTICSEARCH_DATA_INDEX'],
                                                        SystemEnv['ELASTICSEARCH_DATA_TYPE']
                                                        )
        es_list = requests.get(Data_urls)
        data = json.loads(es_list.text)
        print(data['hits']['hits']['total'])
    elif Pass == 'cookie':
        Cookie_urls = "{}/{}/{}/_search?size={}".format(SystemEnv['ELASTICSEARCH_DB_SERVER'],
                                                      SystemEnv['ELASTICSEARCH_COOKIE_INDEX'],
                                                      SystemEnv['ELASTICSEARCH_COOKIE_TYPE'],
                                                      SystemEnv['QUERY_DATA_NUMBER'])
        es_list = requests.get(Cookie_urls)
        data = json.loads(es_list.text)
        print(data)