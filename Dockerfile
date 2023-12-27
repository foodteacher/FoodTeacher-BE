FROM python:3.9
ENV MYSQL_HOST=10.111.96.92
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=foodteacher123
ENV MYSQL_DATABASE=mysql
ENV MYSQL_USER=user1
ENV MYSQL_PASSWORD=foodteacher123

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
