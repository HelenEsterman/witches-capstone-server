from django.db import models


class SpellIngredient(models.Model):
    spell = models.ForeignKey("Spell", on_delete=models.CASCADE, related_name="spells_ingredients")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, related_name="spells_ingredients")
    measurement = models.CharField(max_length=300, blank=True)