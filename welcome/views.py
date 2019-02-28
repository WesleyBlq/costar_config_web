from django.shortcuts import render
from django.http import HttpResponse
import configparser
from subprocess import call
import re
import datetime

config_file_path = "../bhw_cos_gateway/config.ini"

# Create your views here.
def welcome(request):
    title="costar系统配置"

    cfg = configparser.ConfigParser()
    cfg.read(config_file_path, encoding = 'utf-8-sig')
    host_ip = cfg.get("server", "ip")
    mac_addr = cfg.get("server", "mac_addr")
    
    gateway = cfg.get("server", "gateway")
    UPS_ip = cfg.get("server", "ups_ip")
    camera_type = cfg.get("server", "camera_type")
    serial_num = cfg.get("server", "serial_num")
    default_focus_speed = cfg.get("camera", "default_focus_speed")
    infra_open = cfg.get("timing", "infra_open")
    infra_close = cfg.get("timing", "infra_close")

    # ISOTIMEFORMAT = 
    sys_time = datetime.datetime.now().strftime('%H:%M')

    return render(request, 'welcome.html', {'title': title, "host_ip": host_ip, \
        "UPS_ip": UPS_ip, "gateway": gateway, "camera_type": camera_type, \
        "default_focus_speed": default_focus_speed, "serial_num": serial_num, \
        "mac_addr": mac_addr, "infra_open": infra_open, "infra_close": infra_close, "sys_time": sys_time})

def change(request):
    # return 

    host_ip = request.GET["host_ip"]
    UPS_ip = request.GET["UPS_ip"]
    gateway = request.GET["gateway"]
    camera_type = request.GET["camera_type"]
    serial_num = request.GET["serial_num"]
    mac_addr = request.GET["mac_addr"]
    sys_time = request.GET["sys_time"]
    infra_open = request.GET["infra_open"]
    infra_close = request.GET["infra_close"]
    

    cfg = configparser.ConfigParser()
    cfg.read(config_file_path, encoding = 'utf-8-sig')
    cfg.set("server", "ups_ip", UPS_ip)
    cfg.set("server", "ip", host_ip)
    cfg.set("server", "gateway", gateway)
    cfg.set("server", "camera_type", camera_type)
    cfg.set("server", "serial_num", serial_num)
    cfg.set("server", "mac_addr", mac_addr)
    cfg.set("timing", "infra_open", infra_open)
    cfg.set("timing", "infra_close", infra_close)

    cfg.write(open(config_file_path, "w"))
    
    # 修改linux系统固定IP
    content = None
    with open('/etc/network/interfaces') as fh:
        content = fh.read()
        content = re.sub("address " + r'*.*.*.*', "address " + host_ip, content)
        content = re.sub("gateway " + r'*.*.*.*', "gateway " + gateway, content)

    with open('/etc/network/interfaces', 'w') as fw:
        fw.write(content)

    content = None
    with open('/etc/init.d/S50costar') as fh:
        content = fh.read()
        # modify mac address
        content = re.sub(r'''([0-9A-F]{1,2}[:]){5}([0-9A-F]{1,2})''',
                        mac_addr,
                        content)

        # modify gateway                        
        # print(content)
        content = re.sub("gw " + r'*.*.*.*',
                         "gw " + gateway, content)
        # print(content)                

    with open('/etc/init.d/S50costar', 'w') as fw:
        fw.write(content)
    #
    # reboot the system
    #
    import os
    cmd = "date -s " + sys_time
    os.system("date -s " + sys_time)
    os.system("hwclock -w")
    call('reboot')

    return HttpResponse("success")
