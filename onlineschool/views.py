from django.shortcuts import render
from django.http import HttpResponse

def aisatsu(request):
    params = {
        'title':'Hello World',
        'msg':'名前を入力してください',
    }
    return render(request,'onlineschool/index.html', params)


def form(request):
    msg = request.POST['msg']
    params = {
        'title':'Hello World',
        'msg':'hello '+msg+'!',
    }
    return render(request,'onlineschool/index.html', params)