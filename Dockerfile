FROM registry.aliyuncs.com/slzcc/python:3
RUN git clone -b docker https://github.com/slzcc/Scrapy-Zhihu.git && \
    pip install -r package.txt && \
    cd Scrapy-Zhihu && \

ENV REDIS_DB_HOST=127.0.0.1 \
    REDIS_DB_PORT=6379 \
    MONGODB_DB_HOST=127.0.0.1 \
    MONGODB_DB_PORT=27017

CMD ["python", "main.py"]
