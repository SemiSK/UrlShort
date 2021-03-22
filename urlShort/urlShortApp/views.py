import hashlib
import requests
from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .models import ShortUrl, CounterModel
from .forms import FullUrlForm
from django.utils import timezone
import datetime
from urlShort.settings import BASE_DIR
import os
from urllib.parse import urlsplit
from django.contrib.auth.decorators import login_required
from django.core import serializers

expiry_delta = datetime.timedelta(days=21)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def urlApi(request, shrt_url):
    try:
        urlObject = ShortUrl.objects.get(hashedUrl=shrt_url)
        longUrl = urlObject.fullUrl
        urlObject.clicks += 1
        urlObject.save()
        return HttpResponseRedirect(longUrl)
        # return HttpResponse("You're looking at url %s." % longUrl)
    except Exception as e:
        raise Http404(e)

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
                # Build parameters for the ShortUrl object.
                full_base_url = request.build_absolute_uri(reverse('index'))
                salted_url = '{}{}'.format(counter.count, full_url)
                hashed_url = hashlib.md5(salted_url.encode()).hexdigest()[:7]
                expiry_date = timezone.now() + expiry_delta
                
                # Create url entry with user relation if authenticated.
                if request.user.is_authenticated:
                    shortened_url = ShortUrl(fullUrl=full_url, hashedUrl=hashed_url, expire_date= expiry_date, owner= request.user).save()    
                else:
                    shortened_url = ShortUrl(fullUrl=full_url, hashedUrl=hashed_url, expire_date= expiry_date).save()     
                
                # Build the shortened url.
                full_short_url = full_base_url + hashed_url
                
                # return rendered page with shortened url.
                return render(request, 'urlShortApp/short_url.html', {'full_short_url': full_short_url})
            except shortened_url.DoesNotExist as exception:
                HttpResponse("Hello, world. You're at the polls index.")
                # raise Http404() from exception
    else:
        form = FullUrlForm()
    
    return render(request, 'urlShortApp/shortener_form.html', {'form': form})

@login_required
def userProfile(request):
    if request.method == 'GET':
        # Get all urls for user as list.
        user_urls = list(ShortUrl.objects.filter(owner=request.user).values())

        # TODO Change to template render
        return JsonResponse({'data': user_urls})