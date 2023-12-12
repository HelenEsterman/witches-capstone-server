from django.db import models


class WitchInventory(models.Model):
    witch = models.ForeignKey("Witch", on_delete=models.CASCADE, related_name="witch_inventory")