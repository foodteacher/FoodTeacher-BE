FROM python:3.9
ENV MYSQL_HOST=default-mysql-service-0bdfe-21176413-7825c887ec7e.kr.lb.naverncp.com
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=fastapi_mysql
ENV MYSQL_USER=example
ENV MYSQL_PASSWORD=root
ENV CLOVA_HOST=https://clovastudio.stream.ntruss.com/
ENV CLOVA_API_KEY=NTA0MjU2MWZlZTcxNDJiY+K9lasPWEhdfaOUwcAk3CXlZbbuk6gzXCmOklcibpuN1/NHLmLSOVly+u2MhdZ7iRnikd20xCh3AZYK4dwG5Wp2OD0DXvkn9mPAes9o7F7+Th+yeD1UoCESwjNbJ7WYy8PxOmGxscDVTI8RERpQh1Btrdvbbo6AQ++xrLsF1roKOkAxT6Ux3FJGUdoiVEWqwioku6ksPf4ov6fvrZUyKZA=
ENV CLOVA_API_KEY_PRIMARY_VAL=3NxiPMlcuPlUytdAbAeMLg10eZwrwgQ4FNxYRTeh
ENV CLOVA_REQUEST_ID=b214922245dd443faa37fb0eb3953a70
ENV SECRET_KEY=16efadc5642ffc2bcd01018db441dc68cff66b6e5630d23108e8c7d596f03555
ENV ALGORITHM=HS256
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
