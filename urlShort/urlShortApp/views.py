from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from .models import ShortUrl
import requests
import hashlib 

count_url = 'http://127.0.0.1:8000/count/'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def urlApi(request, shrt_url):
    try:
        longUrl = ShortUrl.objects.get(hashedUrl=shrt_url).fullUrl
        return HttpResponse("You're looking at url %s." % longUrl)
    except:
        raise Http404()

def shortenUrl(request, long_url):
    try:
        count = requests.get(count_url)
        salted_url = '{}{}'.format(count.text, long_url)
        hashed_url = hashlib.md5(salted_url.encode()).hexdigest()[:7]
        ShortUrl(fullUrl=long_url, hashedUrl=hashed_url).save()
        return HttpResponse("You're looking at url %s.      hash: %s" % (salted_url, hashed_url))
    except:
        raise Http404() 
    # return HttpResponse("You'r shorten URL is: %s" % long_url)