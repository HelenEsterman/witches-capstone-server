from django.db import models


class WitchInventoryEquipment(models.Model):
    inventory = models.ForeignKey("WitchInventory", on_delete=models.CASCADE, related_name="inventory_equipment")
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name="witches_inventory_equipment")
    quantity = models.IntegerField(default=0)
    added_on = models.DateField(auto_now_add=True)