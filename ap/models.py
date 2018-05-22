from django.db import models

# Create your models here.


class P(models.Model):
    name = models.CharField(max_length=100)

class M(models.Model):
    root = models.ForeignKey('P', related_name='list', on_delete=models.CASCADE)