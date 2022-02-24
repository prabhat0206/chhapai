from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Orders(models.Model):
    oid = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(max_length=200)
    tax = models.FloatField()
    design = models.ImageField(upload_to = "designs/", null=True, blank=True)
    delivery_date = models.DateField()
    isDelivered = models.BooleanField(default=False)
    isEmailing = models.BooleanField(default=False)


class Jobs(models.Model):
    jid = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    notes = models.TextField()
    unit_cost = models.IntegerField()
    total_cost = models.IntegerField()
    comitted_date = models.CharField(max_length=100)
    discount = models.IntegerField(default=0)


class Stages(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class MidOrder(models.Model):
    mid = models.AutoField(primary_key=True)
    stage = models.ForeignKey(Stages, on_delete=models.CASCADE)
    expected_datetime = models.CharField(max_length=200)
    notes = models.TextField()
    jobs = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    isDone = models.BooleanField(default=False)
    assigned_staff = models.ForeignKey(User, on_delete=models.CASCADE)
