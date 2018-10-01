# encoding: utf-8
from requests import post,get
from datetime import datetime
from flask_monitor_agent.conf import server_port, server_url
from flask_monitor_agent.utils import get_hostname, get_ip_address, get_cpu_percent, get_mem_percent, get_cpu_core_num, \
    get_memory


def get_server_status(server_id):
    """
    通过get方法获取服务器linuxServer的最新状态
    :param server_id: 需要获取的服务器信息
    :return:
    """
    res = get(url='http://{0}:{1}/LinuxServer'.format(server_url, server_port),
              data={'server_id': server_id}
              )
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
    cpu_percent = get_cpu_percent()
    mem_percent = get_mem_percent()
    cpu_core_num = get_cpu_core_num()
    memory = get_memory()
    collect_time = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
    res = post(url='http://{0}:{1}/LinuxServer'.format(server_url, server_port),
               data={'hostname': hostname,
                     'ip_addr': ip_addr,
                     'mem_percent': mem_percent,
                     'cpu_percent': cpu_percent,
                     'collect_time': collect_time,
                     'cpu_core_num': cpu_core_num,
                     'memory': memory},
               # 添加认证header，通过token进行认证
               headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzODM2MzcxNSwiZXhwIjoxNTM4MzY5NzE1fQ.eyJ1c2VyX2lkIjoxfQ.ev2ghGRaWW-laiUB-vLNYQZkMfQgsz9cd4OtdUR2L1E'}
              )
    print(res.status_code)
    print(res.text)



if __name__ == '__main__':
    # post(url='http://127.0.0.1/LinuxServer', data={''})
    # get_server_status(1)
    upload_server_status()