from requests import request
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from .form import *
from staff.models import User
from django.views.generic import DetailView
from django.http import HttpResponse
from staff.pdfgen import get_pdf_from_template
# from django.utils.decorators import method_decorator
# from config.common import allowed_users
from django.db.models import Q


# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_staff)


class CheckToken(generics.ListAPIView):
    queryset = Orders.objects
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return Response({"Success": True})


class OrderView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerWithJobs
    permission_classes = [IsAdminUser, ]


class OrderViewWithStatus(generics.ListAPIView):

    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerwithStatus
    permission_classes = [IsAdminUser, ]


class PendingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsAdminUser, ]

    def get_queryset(self,  *args, **kwargs):
        return super(PendingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder')).filter(no_assign_order=0)


class ProccessingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsAdminUser, ]

    def get_queryset(self, *args, **kwargs):
        return super(ProccessingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order__gt=0).filter(models.Q(midorder__isDone=False))


class CompletedOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsAdminUser, ]

    def get_queryset(self, *args, **kwargs):
        return super(CompletedOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order__gt=0).filter(~models.Q(midorder__isDone=False))


class UserViewAPI(generics.ListAPIView):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializerWithGroup
    permission_classes = [IsAdminUser, ]


class PaymentViewAPI(generics.ListAPIView):

    queryset = Payments.objects.all().order_by('-pid')
    serializer_class = PaymentSerializerWithJob
    permission_classes = [IsAdminUser, ]


class StageViewAPI(generics.ListCreateAPIView):

    queryset = Group.objects.all().exclude(name__contains="payment")
    serializer_class = StagesSerializer
    permission_classes = [IsAuthenticated, ]


class ChallansAPI(generics.ListCreateAPIView):

    queryset = Challans.objects.all().order_by('-cid')
    serializer_class = ChallanSerializerwithJob
    permission_classes = [IsAdminUser, ]


class MyJobsApi(generics.ListAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithStatus
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return super().get_queryset().order_by('-jid').filter(overseer=self.request.user)


class OrderTypeApi(generics.ListAPIView):

    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    permission_classes = [IsAuthenticated, ]


class UserSearchAPI(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, key):
        instance = self.get_queryset()\
            .filter(Q(name__icontains=key) | Q(username__icontains=key) | Q(email__icontains=key) | Q(ph_number__icontains=key))
        serialized = self.serializer_class(instance, many=True).data
        paginated = self.paginate_queryset(serialized)
        return self.get_paginated_response(paginated)


class JobSearchAPI(generics.ListAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithStatus
    permission_classes = [IsAuthenticated, ]

    def get(self, request, key):
        instance = self.get_queryset()\
            .filter(Q(job_name__icontains=key) | Q(item__icontains=key) | Q(description__icontains=key) | Q(order__customer_name__icontains=key))
        serialized = self.serializer_class(instance, many=True).data
        paginated = self.paginate_queryset(serialized)
        return self.get_paginated_response(paginated)


class ChallanPdfResponse(DetailView):
    queryset = Challans.objects.all()
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        data = ChallanSerializerwithJob(instance).data
        data['order_date_time'] = instance.job.order.date_time.strftime(
            '%Y-%m-%d, %H:%M:%S')
        data['date_time'] = instance.date_time.strftime('%Y-%m-%d, %H:%M:%S')
        pdf = get_pdf_from_template(self.template_name, data)
        return HttpResponse(pdf, content_type='application/pdf')


class PaymentPdfResponse(DetailView):
    queryset = Payments.objects.all()
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        data = PaymentSerializerWithJob(instance).data
        data['order_date_time'] = instance.job.order.date_time.strftime(
            '%Y-%m-%d, %H:%M:%S')
        data['date_time'] = instance.date_time.strftime('%Y-%m-%d, %H:%M:%S')
        pdf = get_pdf_from_template(self.template_name, data)
        return HttpResponse(pdf, content_type='application/pdf')


class JobDetailPdfResponse(DetailView):
    queryset = Jobs.objects.all()
    template_name = "details.html"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        data = JobWithFullDetails(instance).data
        data['order_date_time'] = instance.order.date_time.strftime(
            '%Y-%m-%d, %H:%M:%S')
        pdf = get_pdf_from_template(self.template_name, data)
        return HttpResponse(pdf, content_type='application/pdf')


