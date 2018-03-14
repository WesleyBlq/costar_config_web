from django.shortcuts import render

# Create your views here.
def welcome(request):
    title="costar系统配置"
    host_ip = "192.168.0.100"
    UPS_ip = "192.168.0.98"
    return render(request, 'welcome.html', {'title': title, "host_ip": host_ip, "UPS_ip": UPS_ip})