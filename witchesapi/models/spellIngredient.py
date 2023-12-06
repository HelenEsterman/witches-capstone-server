from django.db import models


class SpellIngredient(models.Model):
    label = models.CharField(max_length=200)