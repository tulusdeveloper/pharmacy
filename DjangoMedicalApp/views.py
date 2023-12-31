from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from DjangoMedicalApp.models import Company, CompanyBank, Medicine, MedicalDetails
from DjangoMedicalApp.serializers import CompanyBankSerializer, CompanySerializer,MedicalDetailsSerializer, MedicineSerializer, MedicalDetailsSerializerSimple

# Create your views here.


class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict = {"error": False, "message": "Company Data Saved successfully"}
        except:
            response_dict = {"error": True, "message": "Error During Saving Company Data"}
        return Response(response_dict)
    
    def update(self, request,pk=None):
        try:
            queryset=Company.objects.all()
            company=get_object_or_404(Company, pk=pk)
            serializer=CompanySerializer(company,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Data Updated successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
        return Response(dict_response)
    
class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Bank Data Saved successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Bank Data"}
        return Response(dict_response)
    
    def list(self, request):
        Companybank=CompanyBank.objects.all()
        serializer=CompanyBankSerializer(
            Companybank, many=True, context={"request": request})
        response_dict = {
            "error": False,"message": "All Company Bank List Data", "data": serializer.data}
        return Response(response_dict)
    
    def retrieve(self, request,pk=None):
        queryset = CompanyBank.objects.all()
        Companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(Companybank,context={"request": request})
        return Response({"error": False,"message":"Single Data Fetch","data":serializer.data})
    
    def update(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated Successfully"})
    

class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Company.objects.filter(name=name)

class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id=serializer.data['id']
            # Access The Serializer Id saved in our DATABASE TABLE
            # print(medicine_id)

            # Adding and Saving Id into Medicine Details Table
            medicine_details_list=[]
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                # Adding medicine id which will work for medicine details serializer
                medicine_detail["medicine_id"]=medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2=MedicalDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error": False, "message": "Medicine Data Saved successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Medicine Data"}
        return Response(dict_response)
    
    def list(self,request):
        medicine=Medicine.objects.all()
        serializer=MedicineSerializer(medicine,many=True,context={"request":request})

        medicine_data=serializer.data
        newmedicinelist=[]

        # Adding extra Key for Medicine Details in Medicine
        for medicine in medicine_data:
            # Accessing All the Medicine Details of Current Medicine ID
            medicine_details=MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers=MedicalDetailsSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"]=medicine_details_serializers.data
            newmedicinelist.append(medicine)

        response_dict={"error":False,"message": "All Medicine List Data","data":newmedicinelist}
        return Response(response_dict)
    
    def retrieve(self, request,pk=None):
        queryset = Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerializer(medicine,context={"request": request})

        serializer_data=serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        medicine_details=MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializers=MedicalDetailsSerializerSimple(medicine_details,many=True)
        serializer_data["medicine_details"]=medicine_details_serializers.data
        

        return Response({"error": False,"message":"Single Data Fetch","data":serializer_data})

        
    
    def update(self,request,pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerializer(medicine,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated Successfully"})





company_list = CompanyViewSet.as_view({"get": "list"})
company_creat=CompanyViewSet.as_view({"post":"create"})
company_update=CompanyViewSet.as_view({"put":"update"})
