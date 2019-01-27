from django.shortcuts import render
from django.contrib.auth.models import User
from notification.models import *
from django.http import JsonResponse
from django.views import View
import json
from authentication.models import *
from django.utils import timezone
# Create your views here.
class Get_Notification(View):
    def get(self,request,f,t,user_id,token):
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

        notif = Notification.objects.filter(owner=user,read=False).values(
        'sender__first_name',
        'sender__last_name',
        'msg',
        'date'
        )[f:t]

        if len(notif)==0:
            return JsonResponse({'success':False,'error':'went over min or max','error_code':1})

        return JsonResponse({'success':True,'notif':json.dumps(list(notif),default=str)})
