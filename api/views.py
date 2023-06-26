from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer
from typing import List
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def getData(request) -> List:
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True) # set many to tell that we want to seialize multiple items
    return Response(serializer.data)

@api_view(['POST'])
def addData(request) -> List:
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # return all of the objects in here
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True) # set many to tell that we want to seialize multiple items

    return Response(serializer.data)

@api_view(['PUT'])
def updateData(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def deleteData(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    item.delete()
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
    