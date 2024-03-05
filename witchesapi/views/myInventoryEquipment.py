from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchInventoryEquipment


# define inventory equipment serializer
class MyInventoryEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitchInventoryEquipment
        fields = ['id','inventory', 'equipment', 'quantity', 'added_on']


class MyInventoryEquipmentViewSet(viewsets.ViewSet):
    def list(self, request):
        # get only the equipment in 'my' inventory
        myInventoryEquipment = WitchInventoryEquipment.objects.filter(inventory_id=request.auth.user.id)
        # serialize into json format
        serializer = MyInventoryEquipmentSerializer(myInventoryEquipment, many=True, context={'request':request})
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        try:
            # grab equipment obj from database w/ specific pk AND is owned by 'me'
            myInventoryEquipment = WitchInventoryEquipment.objects.get(pk=pk, inventory_id=request.auth.user.id)
            # serialize into json format
            serializer = MyInventoryEquipmentSerializer(myInventoryEquipment, many=False, context={'request':request})
            return Response(serializer.data)
        # error handle if equipment not found
        except WitchInventoryEquipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def create(self,request):
        # get values of data from HTTP request body
        equipment_id = request.data['equipment']
        quantity = request.data['quantity']
        inventory_id = request.auth.user.id

        # check if there is already a piece of equipment in the inventory with same user id and equipment id (ensures no duplicate)
        existing_equipment = WitchInventoryEquipment.objects.filter(inventory_id = inventory_id, equipment_id = equipment_id).first()
        # ^ will return the existing equipment obj or 'None'
        if existing_equipment:
            # if it duplicate exists, just update quantity
            existing_equipment.quantity = quantity
            existing_equipment.save()
            # serialize into json format
            serializer = MyInventoryEquipmentSerializer(existing_equipment, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK) 
        else:
            pass