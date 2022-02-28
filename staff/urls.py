from django.urls import path
from .views import *

urlpatterns = [
    path('order', AddOrderAPi.as_view(), name='order'),
    path('assign_order', AssignOrderJob.as_view(), name='assign_order'),
]
