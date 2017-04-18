FROM registry.aliyuncs.com/slzcc/python:3
RUN git clone -b docker-elasticsearch https://github.com/slzcc/Scrapy-Zhihu.git && \
    cd Scrapy-Zhihu && \
    pip install -r package.txt

ENV REDIS_DB_HOST=127.0.0.1 \
    REDIS_DB_PORT=6379 \
    ELASTICSEARCH_DB_SERVER=http://localhost:9200 \
    ELASTICSEARCH_COOKIE_INDEX=scrapy-cookie \
    ELASTICSEARCH_COOKIE_TYPE=item \
    ELASTICSEARCH_DATA_INDEX=scrapy-zhihu \
    ELASTICSEARCH_DATA_TYPE=item \
    QUERY_ACCOUNT_NUMBER=100 \
    QUERY_DATA_NUMBER=5 \
    TimeCounter=60

WORKDIR /Scrapy-Zhihu

CMD ["python", "main.py"]