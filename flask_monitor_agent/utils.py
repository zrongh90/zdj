# encoding: utf-8
# 定义agent使用的所有方法，例如如何获取hostname,IP等
import socket


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