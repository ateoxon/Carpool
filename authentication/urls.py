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
from authentication.views import *

urlpatterns = [
    path('logout',Logout.as_view()),
    path('login',Login.as_view()),
    path('register',Register.as_view()),
    path('info/<int:user_id>/<str:token>',Get_User_Info.as_view()),
    path('info/update',Update_Info.as_view()),
    path('info/delete',Delete_Account.as_view())
]
