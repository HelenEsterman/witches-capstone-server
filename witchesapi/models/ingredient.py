from django.db import models


class Ingredient(models.Model):
    label = models.CharField(max_length=200)
    healing_property = models.CharField(max_length=200)
    type = models.ForeignKey("IngredientType", on_delete=models.CASCADE, related_name="ingredients")