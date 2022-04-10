from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('order', AddOrderAPi.as_view(), name='order'),
    path('assign_order/<int:pk>', AssignOrderJob.as_view(), name='assign_order'),
    path('login', obtain_auth_token, name='login'),
    path('user/<int:pk>', UserUpdateDestroyView.as_view(), name='update_user_view'),
    path('user', UserAddView.as_view(), name='add_user_view'),
    path('users/all', UserStaffView.as_view(), name='staff_view'),
    path('job/<int:pk>', JobUpdateDestroyAPI.as_view(), name='job'),
    path('midorder/<int:pk>', MidOrderUpdateDestroyAPI.as_view(), name='midorder'),
    path('groups', GetGroupsAPI.as_view(), name='groups'),
    path('challan', CreateChallanApi.as_view(), name='challan_create'),
    path('challan/<int:pk>', ChallanUpdateDistroy.as_view(), name='challan_update'),
    path('payment', CreatePaymentApi.as_view(), name='payment_create'),
    path('payment/<int:pk>', PaymentUpdateDistroy.as_view(), name='payment'),
    path('stage', AddGroupAPI.as_view(), name='add_stage')
]
