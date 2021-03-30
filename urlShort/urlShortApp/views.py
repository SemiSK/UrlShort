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
from pprint import pprint

expiry_delta = datetime.timedelta(days=21)              # Default lifetime of a link.

def urlApi(request, shrt_url):
    '''
    View that handles the redirection using the shortened url.
    '''

    try:
        # Fetch url object with short hash.
        urlObject = ShortUrl.objects.get(hashedUrl=shrt_url)
        
        # Fetch long url from url object.
        longUrl = urlObject.fullUrl

        # Increment the visitor counter.
        urlObject.clicks += 1
        urlObject.save()

        pprint(request.META)
        # Redirect to full url.
        return HttpResponseRedirect(longUrl)

    except Exception as e:
        raise Http404(e)

def shortenUrl(request):
    '''
    View that handles the url shortening.
    '''
    if request.method == 'POST':
        # Get form data from POST request.
        form = FullUrlForm(request.POST)

        # Validate form.
        if form.is_valid():
            # Get full url from form.
            full_url = form.cleaned_data['full_url']
            try:
                # Get counter.
                counter = CounterModel.objects.last()

                #Create counter if does not exist.
                if not counter:
                    counter = CounterModel(count= 0)
                    counter.save()

                # Increment the salt counter.
                counter.count += 1
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

    else:
        # If not POST request set form to empty form object.
        form = FullUrlForm()
    
    # Render form page.
    return render(request, 'urlShortApp/shortener_form.html', {'form': form})

@login_required
def userProfile(request):
    '''
    Handles the user profile view.
    '''
    if request.method == 'GET':
        # Get all urls for user as list.
        user_urls = list(ShortUrl.objects.filter(owner=request.user).values())
        
        # Remove owner_id from query.
        for val in user_urls:
            val.pop('owner_id', None)

        # Prepare table titles and rows from query.
        titles = list(user_urls[0].keys())
        rows = []
        for url in user_urls:
            row = [url[k] for k in titles]
            rows.append(row)

        # Render template with table.
        return render(request, 'urlShortApp/user_profile.html', {
            'user_urls': user_urls,
            'titles': titles,
            'rows': rows,
            })