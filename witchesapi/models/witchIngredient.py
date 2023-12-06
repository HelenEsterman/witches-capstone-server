from django.db import models


class WitchIngredient(models.Model):
    witch = models.ForeignKey("Witch", on_delete=models.CASCADE, related_name='witchIngredient')
    type = models.ForeignKey("IngredientType", on_delete=models.CASCADE, related_name='witchIngredient')
    label = models.CharField(max_length=200)
    healing_property = models.CharField(max_length=200)