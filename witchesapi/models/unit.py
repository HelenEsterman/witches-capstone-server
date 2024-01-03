from django.db import models


class Unit(models.Model):
    label = models.CharField(max_length=200)