# encoding: utf-8
import psutil
import re
import socket

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
    ip_list = []
    for ka_name, info in psutil.net_if_addrs().items():
        ip_addr = info[1][1]
        if is_valid_ip(ip_addr):
            ip_list.append(info[1][1])
    print(ip_list)


def get_net_seg(gw, mask):
    pass


if __name__ == '__main__':
    get_ati_ka()