from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchInventoryEquipment





class MyInventoryEquipmentViewSet(viewsets.ViewSet):
    def list(self, request):
        # get only the equipment in 'my' inventory
        myInventoryEquipment = WitchInventoryEquipment.objects.filter(inventory_id=request.auth.user.id)
        # serialize into json format
        serializer =