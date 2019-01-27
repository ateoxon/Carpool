from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notif(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner")
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    msg = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return "Sender: {}, Receiver: {}".format(sender.email,owner.email)
