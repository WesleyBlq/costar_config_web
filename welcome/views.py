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
    UPS_ip = cfg.get("server", "ups_ip")
    

    return render(request, 'welcome.html', {'title': title, "host_ip": host_ip, \
        "UPS_ip": UPS_ip})

def change(request):
    host_ip = request.GET["host_ip"]
    UPS_ip = request.GET["UPS_ip"]

    cfg = configparser.ConfigParser()
    cfg.read(config_file_path, encoding = 'utf-8-sig')
    cfg.set("server", "ups_ip", UPS_ip)
    cfg.set("server", "ip", host_ip)
    cfg.write(open(config_file_path, "w"))
    
    with open('/etc/network/interfaces') as fh:
        content = fh.read()
        content = re.sub("address " + r'*.*.*.*', "adress 192.168.100.100", content)
        print(content)
    # call('restart')
    
    return HttpResponse("success")