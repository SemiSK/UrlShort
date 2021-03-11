from django.db import models


# Create your models here.
class ShortUrl(models.Model):
    fullUrl = models.URLField(max_length=400)
    hashedUrl = models.CharField(max_length=200)
    expire_date = models.DateTimeField('expire_date')

    class Meta:
        verbose_name = 'URL Entry'
        verbose_name_plural = 'URL Entries'

    def __str__(self):
        return 'Entry {}'.format(self.hashedUrl)
    