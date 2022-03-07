from django.urls import path
from .views import *

urlpatterns = [
    path('orders', OrderView.as_view(), name='orders'),
    path('pending_orders', PendingOrder.as_view(), name='pending_orders'),
    path('in_process_orders', ProccessingOrder.as_view(), name='in_process_orders'),
    path('completed_orders', CompletedOrder.as_view(), name='completed_orders'),
    path('users', UserViewAPI.as_view(), name='users'),
    path('payments', PaymentViewAPI.as_view(), name='payments'),
    path('stages', StageViewAPI.as_view(), name='stages'),
]

