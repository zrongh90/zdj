from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from flask_monitor.database import Base
from datetime import datetime


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


class LinuxServerModel(Base):
    __tablename__ = '__LinuxServer__'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(50), nullable=False)
    ip_addr = Column(String(50), nullable=False)

    def __init__(self, hostname=None, ip_addr=None):
        self.hostname = hostname
        self.ip_addr = ip_addr

    def __repr__(self):
        return '<LinuxServer:{0}_{1}>'.format(self.hostname, self.ip_addr)


class ServerStatusModel(Base):
    __tablename__ = '__ServerStatus__'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('__LinuxServer__.id'), nullable=False)
    cpu_percent = Column(Float, nullable=True, default=0.0, comment="CPU使用率")
    mem_percent = Column(Float, nullable=True, default=0.0, comment="内存使用率")
    collect_time = Column(DateTime, nullable=False, default=datetime.now(), comment="采集时间")

    def __init__(self, server_id=None, cpu_percent=None, mem_percent=None, collect_time=None):
        self.server_id = server_id
        self.cpu_percent = cpu_percent
        self.mem_percent = mem_percent
        self.collect_time = collect_time

    def __repr__(self):
        return '<ServerStatus:{0}_{1}>'.format(self.server_id, self.collect_time)