FROM python:3.9
ENV MYSQL_HOST=default-mysql-service-2-f5362-21317130-8c88a7f95cb7.kr.lb.naverncp.com
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=mysql3
ENV MYSQL_USER=example3
ENV MYSQL_PASSWORD=root

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
