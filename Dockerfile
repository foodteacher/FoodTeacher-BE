FROM python:3.9
ENV MYSQL_HOST=default-mysql-service-0bdfe-21176413-7825c887ec7e.kr.lb.naverncp.com
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=fastapi_mysql
ENV MYSQL_USER=example
ENV MYSQL_PASSWORD=root
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
