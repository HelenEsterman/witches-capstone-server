from django.db import models


class SpellEquipment(models.Model):
    spell = models.ForeignKey("Spell", on_delete=models.CASCADE, related_name="spells_equipment")
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name="spells_equipment")

