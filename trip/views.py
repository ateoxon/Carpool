from django.contrib.auth.models import User
import json
from authentication.models import *
from django.http import JsonResponse
from django.views import View
from authentication.models import *
from trip.models import *
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from notification.models import *

@method_decorator(csrf_exempt,name='dispatch')
class Add_Trip(View):
    def post(self,request):
        if 'token' not in request.POST or 'user_id' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        token = request.POST['token']
        user_id = int(request.POST['user_id'])

        if User.objects.filter(id=user_id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid user id'})

        user = User.objects.get(id=user_id)

        if User_Token.objects.filter(expired=True,token=token,user=user).exists() is True:
            return JsonResponse({'success':False,'error':'Invalid Token'})

        ut = User_Token.objects.get(expired=False,token=token,user=user)

        current_date = timezone.now()

        if current_date > ut.expiration_date:
            User_Token.objects.filter(expired=False,token=token,user=user).update(expired=True)
            return JsonResponse({'success':False,'error_code':0,'error':'Expired Token'})

        if 'trip_id' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        id = request.POST['trip_id']

        if Trip.objects.filter(id=id).exists() is False:
            return JsonResponse({'success':False,'error':'Invalid trip id'})

        trip = Trip.objects.get(id=id)

        if trip.capacity == 0:
            return JsonResponse({'success':False,'error':'Trip is full'})

        if Trip_Member.objects.filter(trip=trip,member=user).exists() is True:
            return JsonResponse({'success':False,'error':'Already listed in the trip'})

        tm = Trip_Member(trip=trip,member=user)
        tm.save()

        Trip.objects.filter(id=id).update(capacity=F('capacity')-1)

        msg = "{} {} Has Joined Your Trip To {} on {}. His Email is {}. Please Communicate to figure out the details".format(
        user.first_name,user.last_name,trip.to_loc_city,trip.date,user.email
        )

        notif = Notif(owner=trip.user,sender=user,msg=msg)
        notif.save()

        return JsonResponse({'success':True})

class Trip_Details(View):
    def get(self,request,trip_id,user_id,token):
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

        if Trip.objects.filter(id=trip_id).exists() is False:
            return JsonResponse({'success':False,'error':'invalid trip id'})

        trip = Trip.objects.get(id=trip_id)

        tm = Trip_Member.objects.filter(trip=trip).values('member__first_name','member__last_name','member__email')

        return JsonResponse({
        'success':True,
        'from_loc_country':trip.from_loc_country,
        'from_loc_state':trip.from_loc_state,
        'from_loc_city':trip.from_loc_city,
        'to_loc_country':trip.to_loc_country,
        'to_loc_state':trip.to_loc_state,
        'to_loc_city':trip.to_loc_city,
        'date':trip.date,
        'capacity':trip.capacity,
        'first_name':trip.user.first_name,
        'last_name':trip.user.last_name,
        'email':trip.user.email,
        'trip_members':json.dumps(list(tm))
        })

class My_Trip(View):
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

        trip = Trip.objects.filter(user=user).values(
        'id',
        'from_loc_country',
        'from_loc_state',
        'from_loc_city',
        'to_loc_country',
        'to_loc_state',
        'to_loc_city',
        'date',
        'capacity'
        )[f:t]

        if len(trip)==0:
            return JsonResponse({'success':False,'error_code':2,'error':'went over min or max'})

        return JsonResponse({
        'success':True,
        'trips':json.dumps(list(trip),default=str)
        })

@method_decorator(csrf_exempt,name='dispatch')
class Create_Trip(View):
    def post(self,request):
        if 'token' not in request.POST or 'user_id' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys 1'})

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

        if 'from_loc_country' not in request.POST or 'from_loc_state' not in request.POST or 'from_loc_city' not in request.POST or 'to_loc_country' not in request.POST or 'to_loc_state' not in request.POST or 'to_loc_city' not in request.POST or 'capacity' not in request.POST:
            return JsonResponse({'success':False,'error':'Missing Keys'})

        from_loc_country = request.POST['from_loc_country']
        from_loc_state = request.POST['from_loc_state']
        from_loc_city = request.POST['from_loc_city']
        to_loc_country = request.POST['to_loc_country']
        to_loc_state = request.POST['to_loc_state']
        to_loc_city = request.POST['to_loc_city']
        capacity = int(request.POST['capacity'])

        trip = Trip(
        user=user,
        from_loc_country=from_loc_country,
        from_loc_state=from_loc_state,
        from_loc_city=from_loc_city,
        to_loc_country=to_loc_country,
        to_loc_state=to_loc_state,
        to_loc_city=to_loc_city,
        capacity=capacity
        )
        trip.save()

        return JsonResponse({'success':True})

class All_Trip(View):
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

        trip = Trip.objects.all().values(
        'id',
        'date',
        'from_loc_country',
        'from_loc_state',
        'from_loc_city',
        'to_loc_country',
        'to_loc_state',
        'to_loc_city',
        'capacity')[f:t]
        if len(trip)==0:
            return JsonResponse({'success':False,'error':'went over min or max'})

        return JsonResponse({'success':True,'trip':json.dumps(list(trip),default=str)})

@method_decorator(csrf_exempt,name='dispatch')
class Search_Trip(View):
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

        if 'from' not in request.POST or 'to' not in request.POST or 'from_loc_country' not in request.POST or 'from_loc_state' not in request.POST or 'from_loc_city' not in request.POST or 'to_loc_country' not in request.POST or 'to_loc_state' not in request.POST or 'to_loc_city' not in request.POST:
            return JsonResponse({'success':False,'error':'missing keys'})

        f = int(request.POST['from'])
        t = int(request.POST['to'])

        from_loc_country = request.POST['from_loc_country']
        from_loc_state = request.POST['from_loc_state']
        from_loc_city = request.POST['from_loc_city']

        to_loc_country = request.POST['to_loc_country']
        to_loc_state = request.POST['to_loc_state']
        to_loc_city = request.POST['to_loc_city']

        trip = Trip.objects.filter(
        from_loc_country=from_loc_country,
        from_loc_state=from_loc_state,
        from_loc_city=from_loc_city,
        to_loc_country=to_loc_country,
        to_loc_state=to_loc_state,
        to_loc_city=to_loc_city
        ).values(
        'from_loc_country',
        'from_loc_state',
        'from_loc_city',
        'to_loc_country',
        'to_loc_state',
        'to_loc_city',
        'date',
        'capacity',
        'id'
        )[f:t]

        if len(trip)==0:
            return JsonResponse({'success':False,'error_code':2,'error':'went over min or max'})

        return JsonResponse({
        'success':True,
        'trip':json.dumps(list(trip),default=str)
        })
