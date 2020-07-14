#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os
import time
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from teacher_rate import TeacherRate

start_time = None
# config_time = int(os.environ["CONFIG_TIME_1578790800"])
config_time = 1578790800
#
delay_time = int(os.environ["DELAY_TIME"])
# delay_time = 1
# int(os.environ["DELAY_TIME"])

db_url_extract = str(os.environ["DB_URL_EXTRACT"])
# db_url_extract = 'mysql://root:1qazXSW@2019@sp1.dev.native.vn:3306/topicalms?charset=utf8&use_unicode=True'

db_url_load = str(os.environ["DB_URL_LOAD"])
# db_url_load = 'mysql://nvn_knowledge:ZKqC7vNK4HgOxnM7@118.70.223.165:3306/nvn_knowledge_v2?charset=utf8&use_unicode=True'

delay_scheduel = int(os.environ["DELAY_SCHEDUEL"])
# delay_scheduel = 6400

# 'SET @row_number := 0; ' + \
sqldata = str(
              'SELECT teacher_id, FORMAT(AVG(points), 1) as rate_avg, MAX(num) AS number_rate ' + \
              'FROM( SELECT @row_number:= CASE ' + \
              'WHEN @customer_no = teacher_id ' + \
              'THEN @row_number + 1 ' + \
              'ELSE 1 ' + \
              'END ' + \
              'AS num, ' + \
              '@customer_no:= teacher_id teacher_id, ' + \
              'timecreated,points ' + \
              'FROM mdl_rating_class, ' + \
              '(SELECT @customer_no:=0,@row_number:=0) as t ' + \
              'WHERE teacher_id > 0 AND vote = 1 and points > 0 ' + \
              'ORDER BY teacher_id, id DESC ' + \
              ') as ali ' + \
              'WHERE num < 301 ' + \
              'GROUP BY teacher_id ')


def dict2TeacherRate(d):
    v = TeacherRate()
    for k in d.keys():
        setattr(v, k, d[k])
    return v


def extractLoad(db_url, list_data, var):
    engine = create_engine(db_url, connect_args={'connect_timeout': 150}, echo=True)
    conn = engine.connect()
    if var == 0:
        conn.execute(text('TRUNCATE teacher_rating_300;'))
    Session = sessionmaker(bind=conn)
    session = Session()
    i = 0
    time_report = datetime.now()
    updated_time = str(time_report)
    for line in list_data:
        d = dict2TeacherRate(line)
        d.updated_time = updated_time
        session.add(d)
        i += 1
    if i > 0:
        session.commit()
    session.close()
    conn.close()


while True:
    if start_time is None:
        start_time = (int((int(
            datetime.now().timestamp()) - 1578790800) / delay_scheduel)) * delay_scheduel + 1578790800 + config_time
    else:
        if start_time > int(datetime.now().timestamp()):
            time.sleep(delay_time)
        continue

    engine = create_engine(db_url_extract, connect_args={'connect_timeout': 150}, echo=True)
    conn = engine.connect()
    sql = text(
        'SELECT COUNT(DISTINCT teacher_id) FROM mdl_rating_class ra JOIN mdl_tpebbb bb ON ra.room_id = bb.id AND ra.teacher_id>0 and points>0 AND vote=1')
    resultCount = conn.execute(sql)
    count = resultCount.fetchone()[0]
    print("have " + str(count) + " record from extract database")
    if count > 100:
        for var in list(range(int(math.ceil(count / 1500)))):
            sqllimit = text(sqldata + str('LIMIT ') + str(var * 1500) + str(',1500'))
            data = conn.execute(sqllimit)
            # print(data.keys())
            extractLoad(db_url_load, data, var)
    start_time += delay_scheduel
