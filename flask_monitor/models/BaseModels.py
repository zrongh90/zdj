from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, UniqueConstraint
from flask_monitor.database import Base
from sqlalchemy_utils.types.choice import ChoiceType
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_monitor.wsgi import app

db = SQLAlchemy(app)
# TODO: 通过flask migrate 控制数据库初始化/升级
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = '__UserModel__'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120), nullable=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class LinuxServerModel(db.Model):
    __tablename__ = '__LinuxServer__'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(50), nullable=False)
    ip_address = Column(String(50), nullable=False)
    cpu_core_num = Column(Integer, nullable=False, comment='CPU core数目')
    memory = Column(Float, nullable=False, comment='内存大小(MB)')

    def __init__(self, hostname, ip_address, cpu_core_num, memory):
        self.hostname = hostname
        self.ip_address = ip_address
        self.cpu_core_num = cpu_core_num
        self.memory = memory

    def __repr__(self):
        return '<LinuxServer:{0}_{1}>'.format(self.hostname, self.ip_address)


class ServerStatusModel(db.Model):
    __tablename__ = '__ServerStatus__'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('__LinuxServer__.id'), nullable=False)
    cpu_percent = Column(Float, nullable=True, default=0.0, comment="CPU使用率")
    mem_percent = Column(Float, nullable=True, default=0.0, comment="内存使用率")
    # 采集时间+服务器ID需要唯一化
    collect_time = Column(DateTime, nullable=False, default=datetime.now(), comment="采集时间")
    __table_args__ = (UniqueConstraint('collect_time','server_id',name='_server_collect_uq_'),{'extend_existing': True})

    def __init__(self, server_id=None, cpu_percent=None, mem_percent=None, collect_time=None):
        self.server_id = server_id
        self.cpu_percent = cpu_percent
        self.mem_percent = mem_percent
        self.collect_time = collect_time

    def __repr__(self):
        return '<ServerStatus:{0}_{1}>'.format(self.server_id, self.collect_time)


class WASServerModel(db.Model):
    STATUS_CHOICE = {
        (0, 'STOP'),
        (1, 'RUNNING'),
        (2, 'UNKNOWN')
    } # 目前支持三种状态: 0-停止；1-运行中；2-未知
    __tablename__ = '__WASServerModel__'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一键")
    server_id = Column(Integer, ForeignKey('__LinuxServer__.id'), nullable=False)
    was_name = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)
    # status = Column(ChoiceType(STATUS_CHOICE))

    def __init__(self, server_id=None, status=0):
        self.server_id = server_id
        self.status = status

    def __repr__(self):
        return '<WASServer:{0}_{1}>'.format(self.id, self.status)
