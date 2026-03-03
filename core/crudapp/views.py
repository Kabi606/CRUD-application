from django.shortcuts import render
from . models import Aiquest
from . serializers import  UserSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser



#Third party Api code [GET, POST, PUT, DELETE]-----> CRUD Operations
#Professional REST APIs follow this pattern:

# Method	     URL	    Action
# GET	     /userinfo/	     list
# GET	     /userinfo/5	retrieve
# POST	     /userinfo/	    create
# PUT	     /userinfo/5	update
# DELETE	 /userinfo/5	delete

def home(request):
    return render(request, "user_info.html")


def UserInfo(request):
    #Complex Data
    info = Aiquest.objects.all()

    #Python Data
    serializer = UserSerializer(info, many =True)

    #Json data
    json_data = JSONRenderer().render(serializer.data)

    #Json data to user
    return HttpResponse(json_data, content_type = 'application/json')

@csrf_exempt
def PerInfo(request, pk):
    if request.method == "DELETE":
        # Delete record - use pk from URL, not from body
        
        aiq = Aiquest.objects.get(id=pk)  # Use pk from URL
        aiq.delete()
        msg = {'msg': 'Data deleted successfully'}
        json_data = JSONRenderer().render(msg)
        return HttpResponse(json_data, content_type = 'application/json')
    

    #Complex data
    per = Aiquest.objects.get(id = pk)

    #Python data to serializer
    serializer = UserSerializer(per)

    #Json Data
    json_data = JSONRenderer().render(serializer.data)

    #Json to user
    return HttpResponse(json_data, content_type = 'application/json')
    

@csrf_exempt
def UserCreate(request):
    if request.method == "POST":
        json_data = request.body
        #json to stream convert
        stream = io.BytesIO(json_data)
        #stream to python
        python_data = JSONParser().parse(stream)
        #python to complex
        serializer = UserSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Successfully insert data'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        
        json_data = JSONRenderer(),render(serializer.errors)
        return HttpResponse(json_data, content_type = 'application/json')
    
    if request.method == 'PUT':
        json_data = request.body
        #Json to stream
        stream = io.BytesIO(json_data)

        #Stream to python
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        aiq = Aiquest.objects.get(id=id)

        #Python to json data
        serializer = UserSerializer(aiq,data = python_data, partial = True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data update successfully'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'appication/json')
    

    if request.method == 'DELETE':
        json_data = request.body

        #json to stream
        stream = io.BytesIO(json_data)

        #stream to python data
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        aiq = Aiquest.objects.get(id=id)
        aiq.delete()
        msg = {'msg': 'Data deleted successfully'}
        data = JSONRenderer().render(msg)
        return HttpResponse(data, content_type='application/json')



#Function bases api_view

from django.shortcuts import render
from . models import Aiquest
from . serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
    
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def infocreate(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            ai = Aiquest.objects.get(id=id)
            serializer = UserSerializer(ai)
            return Response(serializer.data)
        
        data = Aiquest.objects.all()
        serializer = UserSerializer(data, many = True)
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data insert successfully')
        return Response(serializer.errors)


    if request.method == 'PUT':
        id = pk
        aiq = Aiquest.objects.get(id = id)
        serializer = UserSerializer(aiq, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Full data updated successfully')
        return Response(serializer.errors)
    
    if request.method == 'PATCH':
        id = pk
        aiq = Aiquest.objects.get(id=id)
        serializer = UserSerializer(aiq, request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response('Partial data update successfully')
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        id = pk
        aiq = Aiquest.objects.get(id=id)
        aiq.delete()
        return Response('Data deleted successfully')
        


# Class based api view

from django.shortcuts import render
from . models import Aiquest
from . serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class courseinfo(APIView):
    def get( self,request, pk=None, format=None):
        id = pk
        if id is not None:
            aiq = Aiquest.objects.get(id=id)
            serializer = UserSerializer(aiq)
            return Response(serializer.data)
        data = Aiquest.objects.all()
        serializer = UserSerializer(data, many =True)
        return Response(serializer.data)

    
    def post(self,request, format = None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data created successfully')
        return Response(serializer.errors)
    
    def put(self, request,pk=None, format=None):
        id = pk
        aiq = Aiquest.objects.get(id = id)
        serializer = UserSerializer(aiq, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data updated successfully')
        return Response(serializer.errors)
    
    def patch(self,request,pk=None,format=None):
        id = pk
        aiq = Aiquest.objects.get(id=id)
        serializer = UserSerializer(aiq, request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response('Partial data update successfully')
        return Response(serializer.errors)
    
    def delete(self,request,pk=None,format=None):
        id = pk
        aiq = Aiquest.objects.get(id=id)
        aiq.delete()
        return Response('Data deleted successfully')
    

#Mixin CRUD operation
#Listmodelmixin, Retrivemodelmixin, Createmodelmixin, Updatemodelmixin, Destroymodelmixin

from . models import Aiquest
from . serializers import UserSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView


class ailist(GenericAPIView, ListModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class aiid(GenericAPIView, RetrieveModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

class ailistcreate(GenericAPIView, CreateModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ailistupdate(GenericAPIView, UpdateModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class ailistdelete(GenericAPIView, DestroyModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


# Alternative

from . models import Aiquest
from . serializers import UserSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
    
class coursecreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class courseid(GenericAPIView, RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


#LIstcreateAPiview, RetriveUpdateDestroyApiview

from . models import Aiquest
from . serializers import UserSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class info(ListCreateAPIView):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer

class infoid(RetrieveUpdateDestroyAPIView):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer


#ModelViewset

from . models import Aiquest
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

class Aiquest_model(viewsets.ModelViewSet):
    queryset = Aiquest.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    



#External APP using Python

# userlist.py [ 1 ]

# import requests


# url = "http://127.0.0.1:8000/userinfo/"


# data = requests.get(url = url)
# response = data.json()
# print(response)


#External APP [ 2 ]

#create.py

# import requests
# import json

# url = 'http://127.0.0.1:8000/infocreate/'


# data = {
#     'id': 1,
#     'teacher_name' : 'Luka',
#     'course_name' : 'Freelancing',
#     'course_duration' : 5,
#     'seat' : 40,
# }

# json_data = json.dumps(data)
# r = requests.post(url =url, data = json_data)
# data = r.json()
# print(data)


#External APP [ 3 ]

# update.py

# import requests
# import json


# url = "http://127.0.0.1:8000/infocreate/"


# data = {
#     'id' : 14,
#     'teacher_name': 'Alim',
#     'course_name': 'Ai',
# }

# json_data = json.dumps(data)
# r = requests.put(url=url, data = json_data)
# data = r.json()
# print(data)



#External APP [ 4 ]

# delete.py

# import requests
# import json

# url = 'http://127.0.0.1:8000/usercreate/'


# data = {
#     'id': 22,
# }

# json_data = json.dumps(data)
# r = requests.delete(url=url, data = json_data)
# data = r.json()
# print(data)