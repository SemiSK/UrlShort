import hashlib
import requests
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import ShortUrl
from .forms import FullUrlForm

count_url = 'http://127.0.0.1:8000/count/'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def urlApi(request, shrt_url):
    try:
        longUrl = ShortUrl.objects.get(hashedUrl=shrt_url).fullUrl
        return HttpResponse("You're looking at url %s." % longUrl)
    except:
        raise Http404()

def shortenUrl(request):
    if request.method == 'POST':
        print(request.POST)
        form = FullUrlForm(request.POST)
        if form.is_valid():
            full_url = form.cleaned_data['full_url']
            try:
                count = requests.get(count_url)
                salted_url = '{}{}'.format(count.text, full_url)
                hashed_url = hashlib.md5(salted_url.encode()).hexdigest()[:7]
                shortened_url = ShortUrl(fullUrl=full_url, hashedUrl=hashed_url).save()
                return HttpResponse("You're looking at url %s.      hash: %s" % (salted_url, hashed_url))
            except shortened_url.DoesNotExist as exception:
                raise Http404() from exception
    else:
        form = FullUrlForm()
    
    return render(request, 'urlShortApp/shortener_form.html', {'form': form})
    