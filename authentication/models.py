from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_Token(models.Model):
    token = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()
