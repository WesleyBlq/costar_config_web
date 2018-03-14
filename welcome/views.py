from django.shortcuts import render
from django.http import HttpResponse
import configparser

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
    # ip, port = cfg.get("server", "ups_ip"), int(cfg.get("server", "ups_port"))
    return HttpResponse("success")