from django.shortcuts import render
from django.http import HttpResponse
import configparser
from subprocess import call
import re

config_file_path = "../bhw_cos_gateway/config.ini"

# Create your views here.
def welcome(request):
    title="costar系统配置"

    cfg = configparser.ConfigParser()
    cfg.read(config_file_path, encoding = 'utf-8-sig')
    host_ip = cfg.get("server", "ip")
    gateway = cfg.get("server", "gateway")
    UPS_ip = cfg.get("server", "ups_ip")
    camera_type = cfg.get("server", "camera_type")

    return render(request, 'welcome.html', {'title': title, "host_ip": host_ip, \
        "UPS_ip": UPS_ip, "gateway": gateway, "camera_type": camera_type})

def change(request):
    host_ip = request.GET["host_ip"]
    UPS_ip = request.GET["UPS_ip"]
    gateway = request.GET["gateway"]
    camera_type = request.GET["camera_type"]

    cfg = configparser.ConfigParser()
    cfg.read(config_file_path, encoding = 'utf-8-sig')
    cfg.set("server", "ups_ip", UPS_ip)
    cfg.set("server", "ip", host_ip)
    cfg.set("server", "gateway", gateway)
    cfg.set("server", "camera_type", camera_type)
    cfg.write(open(config_file_path, "w"))
    
    # 修改linux系统固定IP
    content = None
    with open('/etc/network/interfaces') as fh:
        content = fh.read()
        content = re.sub("address " + r'*.*.*.*', "address " + host_ip, content)
        content = re.sub("gateway " + r'*.*.*.*', "gateway " + gateway, content)

    with open('/etc/network/interfaces', 'w') as fw:
        fw.write(content)
    call('reboot')

    return HttpResponse("success")