import optparse
from socket import gethostbyname, gethostbyaddr
import socket
import threading
import nmap

screen_lock = threading.Semaphore(value=1)


def conn_scan(tgt_host, tgt_port):
    # print('scan {0} for port {1}'.format(tgt_host, tgt_port))

    ip_port = (tgt_host, int(tgt_port))
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(ip_port)
        # sk.send(b'test')
        result = sk.recv(1000)
        screen_lock.acquire()
        print('tcp port:{0} is opened!'.format(tgt_port), end='')
        print('{0}'.format(result))
        # sk.close()
    except Exception as e:
        # print(e)
        screen_lock.acquire()
        print('tcp port:{0} is close!'.format(tgt_port))
    finally:
        screen_lock.release()
        sk.close()


def nmap_scan(tgt_host, tgt_port):
    nmap_port_scan = nmap.PortScanner()
    result = nmap_port_scan.scan(hosts=tgt_host, ports=tgt_port)
    # import pdb; pdb.set_trace()
    # print(result)
    # port_info = result['scan'][tgt_host]['tcp'][int(tgt_port)]
    # import pdb;pdb.set_trace()
    if len(result['scan']) == 0:
        # 如果nmap无法扫描到结果，继续
        return
    scan_result = result['scan'][tgt_host]['tcp']
    for one in scan_result.keys():
        port_num = one
        port_result = scan_result.get(one)
        print('port {0}:'.format(port_num), port_result['state'], port_result['product'])
        # print(scan_result.get(one))
    # if port_info['state'] == 'open':
    #     print('port:{0} '.format(tgt_port),port_info['state'], port_info['product'])


def port_scan(tgt_host, tgt_ports):
    try:
        tgt_ip = gethostbyname(tgt_host)
    except:
        print("can't get host {0} ip addr!".format(tgt_host))
        return
    try:
        tgt_name = gethostbyaddr(tgt_ip)
        print('scan result for host:{0}'.format(tgt_name))
    except:
        print('scan result for host:{0}'.format(tgt_ip))
    nmap_scan(tgt_ip, tgt_ports)
    # port_start, port_end = tgt_ports.split('-')
    # socket.setdefaulttimeout(2)
    # for port in range(int(port_start), int(port_end)):
    # # for port in port_list:
    #     t = threading.Thread(target=nmap_scan,args=(tgt_host, str(port)))
    #     t.start()
        # conn_scan(tgt_host, port)


if __name__ == '__main__':
    parser = optparse.OptionParser('Usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost')
    parser.add_option('-p', dest='tgtPort')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPort = options.tgtPort
    if tgtHost is None or tgtPort is None:
        print(parser.usage)
        exit(0)
    print('scan port {0} port {1}'.format(tgtHost, tgtPort))
    port_scan(tgtHost, tgtPort)