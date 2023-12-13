from django.shortcuts import render
from django.contrib.auth.models import User

def test(request):
    #test.htmlをレンダリング
    return render(request,'test.html')

