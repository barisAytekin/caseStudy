from rest_framework import serializers
from myApp.models import User

class UserSerializer(serializers.ModelSerializer):  #sifresiz serialization  icin kullanılacak, response donerken gerekecek
    class Meta:
        model = User
        fields = ("id", "name", "email")

class UserSerializerWithPassword(serializers.ModelSerializer): #sifreli serialization  icin kullanılacak, veritabanina kaydederken gerekecek
    class Meta:
        model = User
        fields = ("id", "name", "email", "password")