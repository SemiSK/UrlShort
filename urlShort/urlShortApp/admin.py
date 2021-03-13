from django.contrib import admin
from .models import ShortUrl, CounterModel

admin.site.register(ShortUrl)
admin.site.register(CounterModel)

