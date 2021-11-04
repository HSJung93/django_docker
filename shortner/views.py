from django.shortcuts import render, redirect
from .models import Url

# Create your views here.

# def shortner(request):
#     return render(request, 'shortner.html')

def create(request):
    if request.method == 'POST':
        full_url = request.POST.get('full_url')
        obj = Url.create(full_url)
        return render(request, 'shortner.html', {
            'full_url' : obj.full_url,
            'short_url' : request.get_host() + '/shortner/' + obj.short_url,
            'only_url' : obj.short_url
        })

    return render(request, 'shortner.html')

def go(request, key):
    try:
        obj = Url.objects.get(short_url=key)
        return redirect(obj.full_url)
    except:
        return redirect(create())