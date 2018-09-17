# encoding: utf-8
# 定义agent使用的所有方法，例如如何获取hostname,IP等
import socket
import psutil

def get_hostname():
    """
    获取hostname，根据系统的/etc/hostname的配置信息
    :return: hostname字符串
    """
    return socket.gethostname()


def get_ip_address():
    """
    获取主机的IP信息，先通过过get_hostname获取主机名，再根据主机名
    在/etc/hosts配置的IP信息去获取主机的IP地址
    :return: ip地址的字符串
    """
    return socket.gethostbyname(get_hostname())


def get_cpu_percent():
    """
    通过psutil的cpu_percent模块获取cpu使用率
    :return: cpu使用率
    """
    return psutil.cpu_percent()


def get_mem_percent():
    """
    通过psutil的virtual_memory模块获取内存的使用情况
    :return: mem使用率
    """
    return psutil.virtual_memory().percent


def get_cpu_core_num():
    """
    通过psutil的cpu_count方法获取CPU的格式
    :return: cpu个数
    """
    return psutil.cpu_count()


def get_memory():
    """
    获取psutil的virtual_memory返回的内存大小，以MB为单位
    :return: 内存大小，以MB为单位
    """
    return psutil.virtual_memory().total/1024/1024