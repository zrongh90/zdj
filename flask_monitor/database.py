# encoding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.ext.declarative import declarative_base
from flask_monitor.models import *

# 数据库对象的基类
Base = declarative_base()
# 初始化数据库连接

engine = create_engine('sqlite:///D:\\test.db', convert_unicode=True, poolclass=SingletonThreadPool)
# 创建数据库session, session对象可视为数据库连接
DB_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()