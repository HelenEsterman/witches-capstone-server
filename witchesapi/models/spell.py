from django.db import models


class Spell(models.Model):
    name = models.CharField(max_length=200)
    intention = models.CharField(max_length=200)
    chant = models.CharField(max_length=500, blank=True)
    repeat_chant = models.IntegerField(default= 0, blank=True)
    when_most_powerful = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    instructions = models.CharField(max_length=500)
    additional_info = models.CharField(max_length=400, blank=True)
    favorite = models.BooleanField(default=False)
    ingredients = models.ManyToManyField("Ingredient", through="SpellIngredient", related_name="spells")
    equipment = models.ManyToManyField("Equipment", through="SpellEquipment", related_name="spell_equipment")