from django.db import models

# Create your models here.

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    quantity = models.IntegerField()
    staff_assign = models.CharField()
    order_type = models.CharField(max_length=200)
    tax = models.FloatField()
    design = models.ImageField(upload_to = "designs/")
    delivery_date = models.DateField()
    isEmailing = models.BooleanField(default=False)
    notes = models.TextField()
    job_name = models.CharField(max_length=100)
