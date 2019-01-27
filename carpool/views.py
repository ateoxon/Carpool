from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from authentication.models import *
from django.utils import timezone

class Index(View):
    def get(self,request,user_id,token):
        if User.objects.filter(id=user_id).exists() is False:
            return render(request,'auth/html/error.html')

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=False,token=token,user=user).exists() is False:
            return render(request,'auth/html/error.html')

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return render(request,'auth/html/error.html')

        return render(request,'auth/html/index.html')

class Auth(View):
    def get(self,request):
        return render(request,'auth/html/auth.html')
