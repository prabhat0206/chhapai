from django.urls import path
from .views import *

urlpatterns = [
    path('user_jobs', UserViewByPermissions.as_view(), name='user_jobs')
]


