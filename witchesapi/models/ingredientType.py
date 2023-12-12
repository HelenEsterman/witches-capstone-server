from django.db import models


class IngredientType(models.Model):
    label = models.CharField(max_length=200)