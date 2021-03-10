from django.db import models

# Create your models here.
class counterModel(models.Model):
    count = models.IntegerField('count')

    def __str__(self):
        return 'Counter Entry'
    