from django.urls import re_path, path
from myApp import views

urlpatterns = [
    path('users', views.userApi),
    path('users/<int:incomingId>', views.userApi),
    re_path(r'^', views.badRequest)

]