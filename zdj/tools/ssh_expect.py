# encoding: utf-8
import pexpect
PROMPT = ['# ', '>>> ', '> ', '\$ ', pexpect.TIMEOUT]


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
    child.sendline(password)
    ret = child.expect(PROMPT)
    if ret != 5:
        child.sendline('cat /etc/passwd | grep root')
        child.expect(PROMPT) 
        print(child.before.decode('utf-8'))

if __name__ == '__main__':
    connect('root', '192.168.100.20', 'hujnhu123')
