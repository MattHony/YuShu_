# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/30 20:45
# @Author : '红文'
# @File : base.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, SmallInteger

db = SQLAlchemy()


class Base(db.Model):
    # create_time = Column('create_time', Interger)
    status = Column(SmallInteger, default=1)
