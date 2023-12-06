from django.db import models


class Spell(models.Model):
    name = models.CharField(max_length=200)
    intention = models.CharField(max_length=200)
    chant = models.CharField(max_length=500)
    when_most_powerful = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    other_instructions = models.CharField(max_length=500)
    favorite = models.BooleanField(default=False)
    ingredients = models.ManyToManyField("SpellIngredient", through="IngredientForSpell", related_name="spells")
