from sqlalchemy import Column, Integer, String
from flask_monitor.database import Base


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