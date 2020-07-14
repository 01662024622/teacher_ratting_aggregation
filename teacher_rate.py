#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class TeacherRate(Base):
    __tablename__ = 'teacher_rating_300'
    id = Column('id', BigInteger, primary_key=True)
    teacher_id = Column('teacher_id', Integer)
    rate_avg = Column('rate_avg', DOUBLE)
    number_rate = Column('number_rate', Integer)
    updated_time = Column('updated_time', TIMESTAMP)