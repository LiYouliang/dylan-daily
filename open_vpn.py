# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import re
import urllib.request
import random


def ip_addr_show():
    print('#' * 10, '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='ip addr'),
          '#' * 10)
    command = ["ip", "addr", "show"]
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)


def ip_route_show():
    print('#' * 10, '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='ip route'),
          '#' * 10)
    command = ["ip", "route", "show"]
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)


def disconnect_vpn():
    print(
        '#' * 10,
        '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='killall pppd'),
        '#' * 10)
    command = ["killall", "pppd"]
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)


def default_gateway(gateway_ip='192.168.10.1'):
    print('#' * 10,
          '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='set default gateway'),
          '#' * 10)
    command = ["ip", "route", 'replace', "default", 'via', gateway_ip]
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)


def change_gateway(dev):
    print('#' * 10, '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                             msg='change default gateway'), '#' * 10)
    command = ["ip", "route", 'replace', "default", 'dev', dev]
    print(' '.join(command))
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)


def call_vpn(vpn_index):
    files = os.listdir('/etc/ppp/peers')
    if vpn_index < len(files):
        vpn_name = files[vpn_index]
        print('#' * 10, '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 msg='call vpn ' + vpn_name), '#' * 10)
        print(files)
        command = ["pppd", "call", vpn_name, "updetach"]
        ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(ps.stderr, ps.stdout)
        result = re.findall(r"Using interface (\w+)", ps.stdout, re.MULTILINE)
        return result[0]
    else:
        print(
            '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='vpn is out index'))
        return None


def change_dns():
    print('#' * 10,
          '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='change DNS'),
          '#' * 10)
    command = ['echo', 'nameserver', '8.8.8.8']
    with open("/etc/resolv.conf", "w") as outfile:
        ps = subprocess.run(command, stdout=outfile)
    # ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stdout, ps.returncode, ps.stderr, ps.args)


def get_external_ip():
    print('#' * 10,
          '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='get external ip'),
          '#' * 10)
    external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    print('external ip: ', external_ip)


def set_vpn(vpn_host='v.oouka.com', user_name='Astrawu', password='900128'):
    print('#' * 10,
          '{now:<20}:{msg}'.format(now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg='connect vpn'),
          '#' * 10)
    vpn_name = vpn_host.replace('.', '_')
    # 加最后一个参数--start意思是配置完后立刻启动。
    command = ["pptpsetup", "--create", vpn_name, "--server", vpn_host, "--username", user_name, "--password", password,
               "--encrypt"]
    ps = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(ps.stderr, ps.stdout)
    files = os.listdir('/etc/ppp/peers')
    print(files)


def main(vpn_index):
    ip_addr_show()
    ip_route_show()

    # 关闭连接并恢复网关
    disconnect_vpn()
    # ip_addr_show()
    default_gateway(gateway_ip='172.31.0.1')

    # 使用vpn并修改网关
    dev = call_vpn(vpn_index)
    if dev is None:
        exit()
    change_gateway(dev)

    # 修改DNS
    change_dns()

    # 测试
    get_external_ip()


def recover_network():
    ip_addr_show()
    ip_route_show()

    # 关闭连接并恢复网关
    disconnect_vpn()
    # ip_addr_show()
    default_gateway(gateway_ip='172.31.0.1')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        vpn_index = random.randrange(1, 10)
        main(vpn_index)
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'recover':
            recover_network()
        elif sys.argv[1] == 'set_vpn':
            set_vpn(vpn_host='v.oouka.com')
            set_vpn(vpn_host='v2.oouka.com')
            set_vpn(vpn_host='v3.oouka.com')
            set_vpn(vpn_host='v4.oouka.com')
            set_vpn(vpn_host='d.oouka.com')
            set_vpn(vpn_host='m.oouka.com')
            set_vpn(vpn_host='s.oouka.com')
            set_vpn(vpn_host='tw2.oouka.com')
            set_vpn(vpn_host='tw3.oouka.com')
        else:
            vpn_index = int(sys.argv[1])
            main(vpn_index)
