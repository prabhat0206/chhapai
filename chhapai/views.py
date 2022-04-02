from rest_framework.response import Response
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAuthenticated, BasePermission
from .serializer import *
from .form import *
from staff.models import User
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
    permission_classes = [IsAuthenticated, ]


class OrderViewWithStatus(generics.ListAPIView):

    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerwithStatus
    permission_classes = [IsAuthenticated, ]


class PendingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self,  *args, **kwargs):
        return super(PendingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder')).filter(no_assign_order=0)


class ProccessingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        return super(ProccessingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
                .filter(no_assign_order__gt=0).filter(isCompleted=False)


class CompletedOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        return super(ChallansAPI, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order__gt=0).filter(~models.Q(midorder__isDone=False))


class UserViewAPI(generics.ListAPIView):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializerWithGroup
    permission_classes = [IsAuthenticated, ]


class PaymentViewAPI(generics.ListAPIView):

    queryset = Payments.objects.all().order_by('-pid')
    serializer_class = PaymentSerializer


class StageViewAPI(generics.ListCreateAPIView):

    queryset = Group.objects.all().exclude(name__contains="payment")
    serializer_class = StagesSerializer


class ChallansAPI(generics.ListCreateAPIView):
    
    queryset = Challans.objects.all().order_by('-cid')
    serializer_class = ChallanSerializer


class MyJobsApi(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithStatus


class OrderTypeApi(generics.ListAPIView):

    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer


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
