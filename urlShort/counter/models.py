from django.db import models

# Create your models here.
class counterModel(models.Model):
    count = models.IntegerField('count')