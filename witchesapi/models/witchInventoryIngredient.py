from django.db import models


class WitchInventoryIngredient(models.Model):
    inventory = models.ForeignKey("WitchInventory", on_delete=models.CASCADE, related_name="inventory_ingredients")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, related_name="witches_inventory_ingredients")
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=200)
    added_on = models.DateField(auto_now_add=True)