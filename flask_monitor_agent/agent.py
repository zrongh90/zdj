# encoding: utf-8
from requests import post,get
from flask_monitor_agent.conf import server_port, server_url
from flask_monitor_agent.utils import get_hostname, get_ip_address


def get_server_status(server_id):
    """
    通过get方法获取服务器linuxServer的最新状态
    :param server_id: 需要获取的服务器信息
    :return:
    """
    res = get(url='http://{0}:{1}/LinuxServer'.format(server_url, server_port),
              params={'server_id': server_id})
    print(res.status_code)
    print(res.text)


def upload_server_status():
    """
    通过post方法将agent的当前信息上传到server端
    :param: hostname主机名
    :param: ip_addr主机IP地址
    :return:
    """
    hostname = get_hostname()
    ip_addr = get_ip_address()
    res = post(url='http://{0}:{1}/LinuxServer'.format(server_url, server_port),
               data={'hostname': hostname,
                     'ip_addr': ip_addr}
              )
    print(res.status_code)
    print(res.text)



if __name__ == '__main__':
    # post(url='http://127.0.0.1/LinuxServer', data={''})
    # get_server_status(1)
    upload_server_status()