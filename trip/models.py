from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    from_loc_country = models.TextField()
    from_loc_state = models.TextField()
    from_loc_city = models.TextField()
    to_loc_country = models.TextField()
    to_loc_state = models.TextField()
    to_loc_city = models.TextField(default="")
    capacity = models.IntegerField()

class Trip_Member(models.Model):
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)
