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
    tax = models.FloatField(default=0.00)
    design = models.ImageField(upload_to = "designs/", null=True, blank=True)
    delivery_date = models.DateField()
    billing_address = models.TextField()


class Jobs(models.Model):
    jid = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    unit_cost = models.IntegerField()
    total_cost = models.IntegerField()
    overseer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comitted_date = models.DateField()
    discount = models.IntegerField(default=0)
    isCompleted = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    isEmailing = models.BooleanField(default=False)
    isOnHold = models.BooleanField(default=False)
    mode = models.CharField(max_length=100, default="normal_mode")


class Stages(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class MidOrder(models.Model):
    mid = models.AutoField(primary_key=True)
    stage = models.ForeignKey(Stages, on_delete=models.CASCADE)
    expected_datetime = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    isDone = models.BooleanField(default=False)
    assigned_staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.order = self.job.order
        super(MidOrder, self).save(*args, **kwargs)

class Challans(models.Model):
    cid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)


class Payments(models.Model):
    pid = models.AutoField(primary_key=True)
    payment_id = models.CharField(max_length=255)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
