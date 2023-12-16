FROM python:3.9
ENV MYSQL_HOST=default-mysql-service-0bdfe-21176413-7825c887ec7e.kr.lb.naverncp.com
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=fastapi_mysql
ENV MYSQL_USER=example
ENV MYSQL_PASSWORD=root
ENV CLOVA_HOST=https://clovastudio.stream.ntruss.com/
ENV CLOVA_API_KEY=NTA0MjU2MWZlZTcxNDJiYzQNPMHi/Vt8f/jUw+uD7CxxbMRCZVRUTctyUOXF4j66TwYR+0rbAlCPe0Gidp9I8H5FHyh/CZdR2nR3P9YLzdyPcQWUoaoBJNdfVdlLRfbApqW6nidfOULcNq8DgkXCDt2ZM3vduRz5ANdNiQE6dExfAsazK9E+7N3ujKbXes6CjsU82BBl6Xgzi+p7xEfKmZauaTerL9hyD591yntGgCg=
ENV CLOVA_API_KEY_PRIMARY_VAL=3NxiPMlcuPlUytdAbAeMLg10eZwrwgQ4FNxYRTeh
ENV CLOVA_REQUEST_ID=1ba64a1d5d5a410b902cf0af1e2a8684
ENV SECRET_KEY="16efadc5642ffc2bcd01018db441dc68cff66b6e5630d23108e8c7d596f03555"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
