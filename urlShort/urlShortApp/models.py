from django.db import models
from django.conf import settings

# Create your models here.
class ShortUrl(models.Model):
    fullUrl = models.URLField(max_length=400)
    hashedUrl = models.CharField(max_length=200)
    expire_date = models.DateTimeField('expire_date')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        null=True,  #Django will store empty values as NULL in the database. Default is False.
        blank=True  #form validation will allow entry of an empty value. Default is False.
    )
    clicks = models.IntegerField('Click count',null=True,default=0)

    class Meta:
        verbose_name = 'URL Entry'
        verbose_name_plural = 'URL Entries'

    def __str__(self):
        return 'Entry {}'.format(self.hashedUrl)


class CounterModel(models.Model):
    count = models.IntegerField('count')

    def __str__(self):
        return 'Counter Entry'