from django.db import models


class IngredientForSpell(models.Model):
    spell = models.ForeignKey("Spell", on_delete=models.CASCADE, related_name='ingredientForSpell')
    spellIngredient = models.ForeignKey("SpellIngredient", on_delete=models.CASCADE, related_name='ingredientForSpell')
