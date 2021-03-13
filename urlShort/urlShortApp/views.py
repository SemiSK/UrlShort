import hashlib
import requests
from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import ShortUrl, CounterModel
from .forms import FullUrlForm
from django.utils import timezone
import datetime
from urlShort.settings import BASE_DIR
import os
from urllib.parse import urlsplit

expiry_delta = datetime.timedelta(days=21)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def urlApi(request, shrt_url):
    try:
        longUrl = ShortUrl.objects.get(hashedUrl=shrt_url).fullUrl
        return HttpResponseRedirect(longUrl)
        # return HttpResponse("You're looking at url %s." % longUrl)
    except:
        raise Http404()

def shortenUrl(request):
    if request.method == 'POST':
        print(request.POST)
        form = FullUrlForm(request.POST)
        if form.is_valid():
            full_url = form.cleaned_data['full_url']
            try:
                counter = CounterModel.objects.last()
                counter.count += 1
                counter.save()
                if not counter:
                    counter = CounterModel(count= 0)
                    counter.save()
            except:
                pass
            try:
                full_base_url = request.build_absolute_uri(reverse('index'))
                salted_url = '{}{}'.format(counter.count, full_url)
                hashed_url = hashlib.md5(salted_url.encode()).hexdigest()[:7]
                expiry_date = timezone.now() + expiry_delta
                shortened_url = ShortUrl(fullUrl=full_url, hashedUrl=hashed_url, expire_date= expiry_date).save()         
                full_short_url = full_base_url + hashed_url
                return render(request, 'urlShortApp/short_url.html', {'full_short_url': full_short_url})
            except shortened_url.DoesNotExist as exception:
                HttpResponse("Hello, world. You're at the polls index.")
                # raise Http404() from exception
    else:
        form = FullUrlForm()
    
    return render(request, 'urlShortApp/shortener_form.html', {'form': form})
    