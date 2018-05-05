# encoding: utf-8
import pexpect
from pexpect import pxssh
PROMPT = [pexpect.TIMEOUT, '# ', '>>> ', '> ', '\$ ']


def run_cmd(child, cmd):
    # expect的字符串可以获取
    ret = child.expect(PROMPT)
    if ret != 0:
        child.sendline(cmd)
        child.expect(PROMPT)
        if ret != 0:
            print(child.before.decode('utf-8'))


def px_run_cmd(px_client, cmd):
    """
    使用pxssh去执行命令
    :param px_client: pxssh的连接handle
    :param cmd: 需要执行的命令
    :return:
    """
    px_client.sendline(cmd)
    px_client.prompt()
    print(px_client.before.decode('utf-8'))


def connect(user, host, password):
    """
    使用账户密码连接到远测的host
    :param user: 用户名
    :param host: 主机host
    :param password: 密码
    :return: pexpect的child对象
    """
    ssh_new_keys = 'Are you sure you want to continue connecting'
    conn_str = 'ssh {0}@{1}'.format(user, host)
    child = pexpect.spawn(conn_str)
    # 连接的三种可能性
    ret = child.expect([pexpect.TIMEOUT, ssh_new_keys, '[P|p]assword'])
    if ret == 0:
        print('Error Connecting!')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword'])
        if ret == 0:
            print('Error Connecting!')
            return
    child.sendline(password)
    return child


def px_connection(user, host, password):
    """
    使用pxssh连接到目标主机
    :param user: 用户名
    :param host: 主机host
    :param password: 密码
    :return:
    """
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print('Error Connecting!')
        exit(0)


if __name__ == '__main__':
    user = "root"
    host = "192.168.100.20"
    password = "hujnhu123"
    # child = connect('root', '192.168.100.20', 'hujnhu123')
    child = px_connection(user, host, password)
    px_run_cmd(child, 'cat /etc/passwd | grep -i root; uname -a')
