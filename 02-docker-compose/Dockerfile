FROM my/first:1
RUN apk add gcc musl-dev mariadb-connector-c-dev 
RUN pip install --upgrade pip
RUN pip install flask_mysqldb flask_httpauth
COPY app.py app.py
