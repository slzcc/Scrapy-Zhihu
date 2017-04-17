FROM registry.aliyuncs.com/slzcc/python:3
RUN git clone -b docker https://github.com/slzcc/Scrapy-Zhihu.git && \
    cd Scrapy-Zhihu && \
    pip install -r package.txt

ENV REDIS_DB_HOST=127.0.0.1 \
    REDIS_DB_PORT=6379 \
    MONGODB_DB_HOST=127.0.0.1 \
    MONGODB_DB_PORT=27017 \
    MONGODB_DB_DBNAME=zhihu \
    MONGODB_DB_DOCNAME=user_information

WORKDIR /Scrapy-Zhihu

CMD ["python", "main.py"]
