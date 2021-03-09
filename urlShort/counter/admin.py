from django.contrib import admin

# Register your models here.
from .models import counterModel

admin.site.register(counterModel)
