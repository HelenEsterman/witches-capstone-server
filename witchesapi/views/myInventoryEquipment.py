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
            pass