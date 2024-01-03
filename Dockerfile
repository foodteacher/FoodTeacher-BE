FROM python:3.9
ENV MYSQL_HOST=34.125.247.54
ENV MYSQL_PORT=8000
ENV MYSQL_ROOT_PASSWORD=foodteacher123
ENV MYSQL_DATABASE=foodteacher
ENV MYSQL_USER=user1
ENV MYSQL_PASSWORD=foodteacher123

ENV SECRET_KEY=15f97448a575823e97d4e8718df130811ef9af4fe1ac6b29bea1f122b1b63ecf

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
