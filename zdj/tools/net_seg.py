# encoding: utf-8
import psutil
from IPy import IP
import socket
import subprocess
import platform

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


def get_ati_ka(platform):
    ef_ip_list = []
    for key, info in psutil.net_if_addrs().items():
        if 'window' in platform.lower():
            ip_addr, net_mask = info[1][1:3]
        elif 'linux' in platform.lower():
            ip_addr, net_mask = info[0][1:3]
        if is_valid_ip(ip_addr):
            if 'window' in platform.lower():
                ret = subprocess.getoutput('ping -n 1 {0}'.format(ip_addr))
                if u"已发送 = 1，已接收 = 1" in ret:
                    ef_ip_list.append((ip_addr, net_mask))
            elif 'linux' in platform.lower():
                ret = subprocess.getoutput('ping -c 1 {0}'.format(ip_addr))
                if "1 packets transmitted, 1 received" in ret:
                    ef_ip_list.append((ip_addr, net_mask))
    return ef_ip_list


def get_net_seg(ip_nm_list):
    for one_tuple in ip_nm_list:
        if one_tuple[1] is not None:
            # 计算IP和NETMASK限定的所有IP列表
            ip = IP(one_tuple[0]).make_net(one_tuple[1])
            all_ip = [one_ip for one_ip in ip]
            print(len(all_ip))


if __name__ == '__main__':
    ef_ip_nm_list = get_ati_ka(platform.platform())
    print(ef_ip_nm_list)
    get_net_seg(ef_ip_nm_list)
