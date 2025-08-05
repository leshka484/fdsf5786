from django.db import models

class JsonItem(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()