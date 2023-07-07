from django.shortcuts import render
from rest_framework import viewsets

from DjangoMedicalApp.models import Company
from DjangoMedicalApp.serializers import CompanySerializer

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
