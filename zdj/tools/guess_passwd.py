# encoding: utf-8
import optparse
import os
from pexpect import pxssh

global Found
Found = False
global target_pwd
target_pwd = ""


def connection(host, user, passwd):
    try:
        s = pxssh.pxssh()
        s.login(host, user, passwd)
        Found = True
        target_pwd = passwd
    except Exception as e:
        print(e)
        print("can't not login!")


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
                print(one_line)
                one_line = f.readline().strip()
    # connection(target_host, target_user, target_pwd_file)
    if Found:
        print("found password:{2} for user:{0} on host:{1}".format(target_user, target_host, target_pwd))
