from django.urls import path
from .views import *
from .stats import *

urlpatterns = [
    path('orders', OrderView.as_view(), name='orders'),
    path('pending_orders', PendingOrder.as_view(), name='pending_orders'),
    path('in_process_orders', ProccessingOrder.as_view(), name='in_process_orders'),
    path('completed_orders', CompletedOrder.as_view(), name='completed_orders'),
    path('users', UserViewAPI.as_view(), name='users'),
    path('payments', PaymentViewAPI.as_view(), name='payments'),
    path('stages', StageViewAPI.as_view(), name='stages'),
    path('last5', Last5Details.as_view(), name='last5'),
    path('counts', HomePageTopStatus.as_view(), name='counts'),
    path('jobs_in_each_stage', JobInEachStage.as_view(), name='jobs_in_each_stage'),
    path('challans', ChallansAPI.as_view(), name='challans'),
    path('jobs', MyJobsApi.as_view(), name='jobs'),
    path('checkauth', CheckToken.as_view(), name='check'),
    path('order_types', OrderTypeApi.as_view(), name='order_types'),
    path('search_job/<key>', JobSearchAPI.as_view(), name='search_job'),
    path('search_user/<key>', UserSearchAPI.as_view(), name='search_user'),
    path('challan/<int:pk>', ChallanPdfResponse.as_view(), name='challans_pdf'),
    path('payment/pdf/<int:pk>', PaymentPdfResponse.as_view(), name='payment_pdf')
]
