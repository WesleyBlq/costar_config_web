from django.shortcuts import render

# Create your views here.
def welcome(request):
    title="costar系统配置"
    return render(request, 'welcome.html', {'title': title,})