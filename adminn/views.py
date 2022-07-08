from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from rest_framework.permissions import BasePermission
from chhapai.serializer import *
from chhapai.form import *
from staff.models import User
from django.db.models import Q
from api.views import job_scheduler
from rest_framework.decorators import api_view, permission_classes


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CheckToken(generics.ListAPIView):
    queryset = Orders.objects
    serializer_class = OrderSerializer
    permission_classes = [IsSuperUser, ]

    def get(self, request, *args, **kwargs):
        return Response({"Success": True})


@api_view(["GET"])
@permission_classes([IsSuperUser])
def update_database(request):
    try:
        job_scheduler()
    except Exception as e:
        print(e)
        pass
    return Response({"Success": True})


class OrderWithoutVendor(generics.ListAPIView):
    queryset = Orders.objects.filter(vendor=None).order_by('-oid')
    serializer_class = OrderSerializer
    permission_classes = [IsSuperUser, ]


class OrderView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerWithJobs
    permission_classes = [IsSuperUser, ]


class AssignVendor(generics.UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsSuperUser, ]


class OrderViewWithStatus(generics.ListAPIView):

    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerwithStatus
    permission_classes = [IsSuperUser, ]


class PendingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsSuperUser, ]

    def get_queryset(self,  *args, **kwargs):
        return super(PendingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder')).filter(no_assign_order=0)


class ProccessingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsSuperUser, ]

    def get_queryset(self, *args, **kwargs):
        return super(ProccessingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order__gt=0).filter(models.Q(midorder__isDone=False))


class CompletedOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsSuperUser, ]

    def get_queryset(self, *args, **kwargs):
        return super(CompletedOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order__gt=0).filter(~models.Q(midorder__isDone=False))


class UserViewAPI(generics.ListAPIView):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializerWithGroup
    permission_classes = [IsSuperUser, ]


class PaymentViewAPI(generics.ListAPIView):

    queryset = Payments.objects.all().order_by('-pid')
    serializer_class = PaymentSerializerWithJob
    permission_classes = [IsSuperUser, ]


class StageViewAPI(generics.ListCreateAPIView):

    queryset = Group.objects.all().exclude(name__contains="payment")
    serializer_class = StagesSerializer
    permission_classes = [IsSuperUser, ]


class ChallansAPI(generics.ListCreateAPIView):

    queryset = Challans.objects.all().order_by('-cid')
    serializer_class = ChallanSerializerwithJob
    permission_classes = [IsSuperUser, ]


class MyJobsApi(generics.ListAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithStatus
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        return super().get_queryset().order_by('-jid').filter(overseer=self.request.user)


class OrderTypeApi(generics.ListAPIView):

    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user)


class UserSearchAPI(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser, ]

    def get(self, request, key):
        instance = self.get_queryset()\
            .filter(Q(name__icontains=key) | Q(username__icontains=key) | Q(email__icontains=key) | Q(ph_number__icontains=key))
        serialized = self.serializer_class(instance, many=True).data
        paginated = self.paginate_queryset(serialized)
        return self.get_paginated_response(paginated)


class JobSearchAPI(generics.ListAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithStatus
    permission_classes = [IsSuperUser, ]

    def get(self, request, key):
        instance = self.get_queryset()\
            .filter(Q(job_name__icontains=key) | Q(item__icontains=key) | Q(description__icontains=key) | Q(order__customer_name__icontains=key))
        serialized = self.serializer_class(instance, many=True).data
        paginated = self.paginate_queryset(serialized)
        return self.get_paginated_response(paginated)


class AddOrderAPi(generics.CreateAPIView):

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsSuperUser, ]

    def post(self, request):
        data = request.data
        new_order = self.serializer_class(data=data)
        if new_order.is_valid():
            new_order.save()
            order = new_order.data
            order['jobs_set'] = []
            for product in request.data.get('jobs'):
                product['order'] = new_order.data['oid']
                jobs = JobSerializer(data=product)
                if jobs.is_valid():
                    jobs.save()
                    order['jobs_set'].append(jobs.data)
            return Response({"Success": True, "order": order})
        return Response({"Success": False})


class AssignOrder(APIView):

    permission_classes = [IsSuperUser]

    def post(self, request, oid):
        order = Orders.objects.get(oid=oid)
        if order:
            order.vendor = request.GET.get("vendor")
            order.save()
            return HttpResponse(200)
        return HttpResponse(404)


class OrdersByVendor(generics.ListAPIView):

    queryset = Orders.objects.all()
    serializer_class = OrderSerializerWithJobs
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.kwargs.get("vendor")).order_by("-oid")


class AddVendor(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]


class AllVendors(generics.ListAPIView):
    queryset = User.objects.all().filter(vendor=True)
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
