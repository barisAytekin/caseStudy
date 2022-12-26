from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from myApp.models import User
from myApp.serializers import UserSerializer, UserSerializerWithPassword
import re

@csrf_exempt
def userApi(request, incomingId = -1): #incomingId url'den alinacak
    if request.method == "GET":
        if incomingId == -1: #adres sadece .../users tan olusuyorsa
            users = User.objects.all()
            user_serializer = UserSerializer(users, many = True) 
            return JsonResponse(user_serializer.data, safe = False) #tum userları response olarak gönder
        else: #adres .../users<id> den olusuyorsa
            user = User.objects.filter(id = incomingId).first()
            if user:
                user_serializer = UserSerializer([user], many = True)
                return JsonResponse(user_serializer.data[0], safe = False) #bulunan user objesini gonder
            else:
                return JsonResponse({"error":"User with that id does not exist"}, safe = False, status = 404) #.filter empty list donuyorsa bu id de user olmadıgına dair response gonder

    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializerWithPassword(data=user_data)
        if user_serializer.is_valid() and incomingId == -1 and request.content_type == "application/json": #adres ve headerlari kontrol et
            if not User.objects.filter(email = user_data["email"]):
                user_serializer.save() #dbye kaydet
                user = User.objects.get(email = user_data["email"])
                user_serializer = UserSerializer([user], many = True) #aynı user ı db den cek ama bu sefer sifresiz serialize et
                return(JsonResponse(user_serializer.data[0], safe = False)) #response
            else: 
                return(JsonResponse({"error": "User with that email already exists"}, safe = False, status = 403)) #aynı emailden bulunma durumu
        else:
            return JsonResponse({"error":"Bad Request"}, safe = False, status = 400)
    elif request.method == "PATCH":
        user_data = JSONParser().parse(request)
        if User.objects.filter(id = incomingId) and request.content_type == "application/json": #adres ve headerlari kontrol et
            user = User.objects.filter(id = incomingId).first()
            user_serializer = UserSerializerWithPassword(user, data = user_data, partial = True)
            if user_serializer.is_valid(): #user modeline uyuyorsa
                user_serializer.save()
                user = User.objects.get(id = incomingId)
                user_serializer = UserSerializer([user], many = True) #aynı user ı db den cek ama bu sefer sifresiz serialize et
                return(JsonResponse(user_serializer.data[0], safe = False)) #response
            else:
                return JsonResponse({"error":"Bad Request"}, safe = False, status = 400) #invalid body durumu
        elif incomingId == -1 or request.content_type != "application/json":
            return JsonResponse({"error":"Bad Request"}, safe = False, status = 400) #invalid adres veya content type durumu
        else:
            return(JsonResponse({"error": "User with that id does not exist"} , safe = False, status = 404)) #user ı bulamama durumu
    elif request.method == "DELETE":
        user_data = JSONParser().parse(request)
        if User.objects.filter(id = incomingId):
            user = User.objects.filter(id = incomingId).first()
            user.delete()
            return HttpResponse(status = 200) #deletion succesful ise bodysiz 200 response u gonder
        elif incomingId == -1:
            return JsonResponse({"error":"Bad Request"}, safe = False, status = 400) #urlde adres bulunmama durumu
        else:
            return(JsonResponse({"error": "User with that id does not exist"} , safe = False, status = 404))#user bulamama durumu
def badRequest(request):
    return JsonResponse({"error":"Bad Request"}, safe = False, status = 400) #diger adresler icin 400 fonksiyonu
def serverError(request):
    return JsonResponse({"error":"server error"}, safe = False, status = 500) #handler500 de kullanılacak fonksiyon
        
         
        