from django.db import models
from staff.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class OrderType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


class Orders(models.Model):
    oid = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    tax = models.FloatField(default=0.00)
    delivery_date = models.DateField()
    billing_address = models.TextField()


class Jobs(models.Model):
    jid = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    design = models.ImageField(upload_to = "designs/", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    unit_cost = models.IntegerField()
    order_type = models.ForeignKey(OrderType, blank=True, null=True, on_delete=models.DO_NOTHING)
    total_cost = models.IntegerField()
    overseer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comitted_date = models.DateField()
    dispatched_quantity = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    isDelivered = models.BooleanField(default=False)
    isEmailing = models.BooleanField(default=False)
    amount_paid = models.IntegerField(default=0)
    isOnHold = models.BooleanField(default=False)
    mode = models.CharField(max_length=100, default="normal_mode")


class MidOrder(models.Model):
    mid = models.AutoField(primary_key=True)
    stage = models.ForeignKey(Group, on_delete=models.CASCADE)
    expected_datetime = models.DateTimeField(blank=True, null=True)
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
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    dispatch_quantity = models.IntegerField(default=0)
    quantity_per_pack = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    no_of_packs = models.IntegerField(default=0)
    generated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=6)

    def save(self, *args, **kwargs):
        self.order = self.job.order
        self.job.dispatched_quantity += self.dispatch_quantity
        self.job.save()
        super(Challans, self).save(*args, **kwargs)


class Payments(models.Model):
    pid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, default="Cash")
    payment_note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=6)

    def save(self, *args, **kwargs):
        self.order = self.job.order
        self.job.amount_paid += int(self.amount)
        self.job.save()
        super(Payments, self).save(*args, **kwargs)
