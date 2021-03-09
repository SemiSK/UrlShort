from django.db import models

# Create your models here.
class ShortUrl(models.Model):
    fullUrl = models.URLField(max_length=400)
    hashedUrl = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now=True)