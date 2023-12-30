from rest_framework import viewsets, status
from rest_framework.response import Response
from witchesapi.models import Unit
from .myInventoryIngredients import UnitSerializer

class UnitViewSet(viewsets.ViewSet):

    def list(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            unit = Unit.objects.get(pk=pk)
            serializer = UnitSerializer(unit, many=False, context={'request': request})
            return Response(serializer.data)

        except Unit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
