from django.shortcuts import render

from rest_framework import generics
from supermarket import models
from .serializers import *

class BasicItemInformationView(generics.ListCreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = BasicItemInformationSerializer

class ItemInstanceView(generics.ListCreateAPIView):
    queryset = models.ItemInstance.objects.all()
    serializer_class = ItemInstanceSerialzer
# Create your views here.
