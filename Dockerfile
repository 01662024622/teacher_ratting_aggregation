FROM python:alpine3.7

RUN pip install requests
RUN pip install sqlalchemy
RUN pip install pymysql
RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev && apk add --no-cache mariadb-dev

RUN pip install mysqlclient  

COPY . /app/teacher-rate-300

WORKDIR /app/teacher-rate-300

CMD python ./main.py