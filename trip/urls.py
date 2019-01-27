"""carpool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from trip.views import *

urlpatterns = [
    path('add',Add_Trip.as_view()),
    path('details/<int:trip_id>/<int:user_id>/<str:token>',Trip_Details.as_view()),
    path('user/<int:f>/<int:t>/<int:user_id>/<str:token>',My_Trip.as_view()),
    path('create',Create_Trip.as_view()),
    path('all/<int:f>/<int:t>/<int:user_id>/<str:token>',All_Trip.as_view()),
    path('search',Search_Trip.as_view())
]
