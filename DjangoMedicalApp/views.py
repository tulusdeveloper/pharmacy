from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from DjangoMedicalApp.models import Company
from DjangoMedicalApp.serializers import CompanySerializer

# Create your views here.


class CompanyViewSet(viewsets.ViewSet):
    def list(self, request):
        company=Company.objects.all()
        serializer=CompanySerializer(
            company, many=True, context={"request": request})
        response_dict = {
            "error": False,"message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            response_dict = {"error": False, "message": "Company Data Saved successfully"}
        except:
            response_dict = {"error": True, "message": "Error During Saving Company Data"}
        return Response(response_dict)


company_list = CompanyViewSet.as_view({"get": "list"})
company_creat=CompanyViewSet.as_view({"post":"create"})