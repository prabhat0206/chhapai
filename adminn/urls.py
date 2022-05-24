from django.urls import path

from adminn.views import *

urlpatterns = [
    path("orders", OrderView.as_view(), name="orders_admin"),
    path('add_order', AddOrderAPi.as_view(), name='order'),
    path("order_by_status", OrderViewWithStatus.as_view(), name="order_status_admin"),
    path('pending_orders', PendingOrder.as_view(), name='pending_orders'),
    path('in_process_orders', ProccessingOrder.as_view(), name='in_process_orders'),
    path('completed_orders', CompletedOrder.as_view(), name='completed_orders'),
    path('users', UserViewAPI.as_view(), name='users'),
    path('payments', PaymentViewAPI.as_view(), name='payments'),
    path('challans', ChallansAPI.as_view(), name='challans'),
    path('jobs', MyJobsApi.as_view(), name='jobs'),
    path('checkauth', CheckToken.as_view(), name='check'),
    path('search_job/<key>', JobSearchAPI.as_view(), name='search_job'),
    path('search_user/<key>', UserSearchAPI.as_view(), name='search_user'),
    path('order_by_vendor/<int:vendor>', OrdersByVendor.as_view(), name='order_by'),
    path('add_vendor', AddVendor.as_view(), name='add_vendor'),
    path('assign_order/<int:oid>', AssignOrder.as_view(), name='assign_order'),
    path('vendors', AllVendors.as_view(), name='vendors'),
]
