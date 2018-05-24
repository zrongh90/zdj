# encoding: utf-8
import psutil
import os
import socket
import subprocess

def is_valid_ip(ip):
    """Returns true if the given string is a well-formed IP address.

    Supports IPv4 and IPv6.
    """
    if not ip or '\x00' in ip:
        # getaddrinfo resolves empty strings to localhost, and truncates
        # on zero bytes.
        return False
    try:
        res = socket.getaddrinfo(ip, 0, socket.AF_UNSPEC,
                                 socket.SOCK_STREAM,
                                 0, socket.AI_NUMERICHOST)
        return bool(res)
    except socket.gaierror as e:
        if e.args[0] == socket.EAI_NONAME:
            return False
        raise
    return True


def get_ati_ka():
    ef_ip_list = []
    for info in psutil.net_if_addrs().items():
        ip_addr = info[1][1][1]
        net_mask = info[1][1][2]
        if is_valid_ip(ip_addr):
            ret = subprocess.getoutput('ping -n 1 {0}'.format(ip_addr))
            if "已发送 = 1，已接收 = 1" in ret or "sended = 1, received = 1":
                ef_ip_list.append((ip_addr, net_mask))
    print(ef_ip_list)



def get_net_seg():
    pass


if __name__ == '__main__':
    get_ati_ka()