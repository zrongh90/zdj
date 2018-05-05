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


def connect(user, host, password):
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
    run_cmd(child, 'cat /etc/passwd | grep -i root')
