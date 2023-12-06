from django.db import models


class SpellIngredient(models.Model):
    label = models.CharField(max_length=200)
    spells = models.ManyToManyField("Spell", through="IngredientForSpell", related_name="spellIngredient")