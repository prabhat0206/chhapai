from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('order', AddOrderAPi.as_view(), name='order'),
    path('assign_order', AssignOrderJob.as_view(), name='assign_order'),
    path('login', obtain_auth_token, name='login'),
    path('user/<int:pk>', UserUpdateDestroyView.as_view(), name='update_user_view'),
    path('user', UserAddView.as_view(), name='add_user_view'),
]
