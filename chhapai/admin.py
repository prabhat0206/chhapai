from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Orders)
admin.site.register(Jobs)
admin.site.register(MidOrder)
admin.site.register(Stages)
admin.site.register(Payments)
admin.site.register(OrderType)
