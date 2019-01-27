from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views import View
from authentication.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.timezone import timedelta

# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class Logout(View):
    def post(self,request):
        if 'token' not in request.POST or 'user_id' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        token = request.POST['token']
        user_id = int(request.POST['user_id'])

        if User.objects.filter(id=user_id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid user id'})

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=False,token=token,user=user).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid Token'})

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return JsonResponse({'success':False,'error_code':0,'error':'Expired Token'})

        User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)

        return JsonResponse({'success':True})

@method_decorator(csrf_exempt,name='dispatch')
class Login(View):
    def post(self,request):
        if 'email' not in request.POST or 'password' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        username = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() is False:
            return JsonResponse({'success':False,'error':'Email doesn\'t exist'})
        else:
            user = User.objects.get(username=username)
            if User_Token.objects.filter(expired=False,user=user).exists() is True:
                tok = User_Token.objects.get(expired=False,user=user)
                if tok.expiration_date < timezone.now():
                    User_Token.objects.filter(expired=False,user=user).update(expired=True)
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        offset = timedelta(days=1)
                        expiration_date = timezone.now() + offset
                        token = get_random_string(length=32)
                        ut = User_Token(
                        token=token,
                        user=user,
                        expiration_date=expiration_date)
                        ut.save()
                        return JsonResponse({'success':True,'token':token,'user_id':user.id})
                    else:
                        return JsonResponse({'success':False,'error':'invalid credentials'})
                return JsonResponse({'success':False,'error':'Already Logged in'})

            user = authenticate(username=username,password=password)
            if user is not None:
                offset = timedelta(days=1)
                expiration_date = timezone.now() + offset
                token = get_random_string(length=32)
                ut = User_Token(
                token=token,
                user=user,
                expiration_date=expiration_date)
                ut.save()
                return JsonResponse({'success':True,'token':token,'user_id':user.id})
            else:
                return JsonResponse({'success':False,'error':'invalid credentials'})

@method_decorator(csrf_exempt,name='dispatch')
class Register(View):
    def post(self,request):
        if 'email' not in request.POST or 'first_name' not in request.POST or 'last_name' not in request.POST or 'password' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        username = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        if User.objects.filter(email=username).exists() is False:
            user = User(
            username = username,
            email = username,
            first_name = first_name,
            last_name = last_name
            )
            user.set_password(password)
            user.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':'User Already Exists'})

class Get_User_Info(View):
    def get(self,request,user_id,token):
        if User.objects.filter(id=user_id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid user id'})

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=False,token=token,user=user).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid Token'})

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return JsonResponse({'success':False,'error_code':0,'error':'Expired Token'})

        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        return JsonResponse({
        'success':True,
        'first_name':first_name,
        'last_name':last_name,
        'email':email
        })

@method_decorator(csrf_exempt,name='dispatch')
class Update_Info(View):
    def post(self,request):
        if 'token' not in request.POST or 'user_id' not in request.POST or 'first_name' not in request.POST or 'last_name' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        token = request.POST['token']
        user_id = int(request.POST['user_id'])

        if User.objects.filter(id=user_id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid user id'})

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=False,token=token,user=user).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid Token'})

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return JsonResponse({'success':False,'error_code':0,'error':'Expired Token'})

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name)
        return JsonResponse({'success':True})

@method_decorator(csrf_exempt,name='dispatch')
class Delete_Account(View):
    def post(self,request):
        if 'token' not in request.POST or 'user_id' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        token = request.POST['token']
        user_id = int(request.POST['user_id'])

        if User.objects.filter(id=user_id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid user id'})

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=False,token=token,user=user).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid Token'})

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return JsonResponse({'success':False,'error_code':0,'error':'Expired Token'})

        User.objects.filter(id=user_id).update(active=False)
        return JsonResponse({'success':True})
