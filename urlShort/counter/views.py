from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from .models import counterModel

def counter_view(request):
    count_object = counterModel.objects.last()
    if count_object is None:
        counterModel(count=0).save()
        count_object = counterModel.objects.last()
    count = count_object.count
    count += 1
    count_object.count = count
    count_object.save()
    return HttpResponse(count)
