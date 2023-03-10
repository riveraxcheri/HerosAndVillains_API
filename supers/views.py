from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import SuperSerializer
from .models import Super

@api_view(['GET', 'POST'])
def supers_list(request):

    if request.method == 'GET':
        super_type = request.query_params.get('super_type')
        queryset = Super.objects.all()

        if super_type:
            queryset = queryset.filter(super_type__type=super_type)
            serializer = SuperSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            custom_response_dictionary= {}
            heroes = Super.objects.filter(super_type__type='Hero')
            villains = Super.objects.filter(super_type__type="Villain")
            for items in heroes:
                serializer = SuperSerializer(heroes, many=True)
                custom_response_dictionary[items.super_type.type] = {
                    "heroes": serializer.data,
                }
            for items in villains:
                serializer = SuperSerializer(villains, many=True)
                custom_response_dictionary[items.super_type.type] = {
                    "villains": serializer.data,
                }
            return Response(custom_response_dictionary)

    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
    supers = get_object_or_404(Super, pk=pk)

    if request.method == 'GET':
        serializer = SuperSerializer(supers);        
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SuperSerializer(supers, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        supers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
