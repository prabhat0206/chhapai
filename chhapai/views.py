from rest_framework import generics
from .models import *
from .serializer import *


class OrderView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerWithJobs


class OrderViewWithStatus(generics.ListAPIView):

    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializerwithStatus


class PendingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer

    def get_queryset(self,  *args, **kwargs):
        return super(PendingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder')).filter(no_assign_order=0)


class ProccessingOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer

    def get_queryset(self, *args, **kwargs):
        return super(ProccessingOrder, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
                .filter(no_assign_order__gt=0).filter(isCompleted=False)


class CompletedOrder(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid').filter(isCompleted=True)
    serializer_class = JobSerializer


class UserViewAPI(generics.ListAPIView):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer


class PaymentViewAPI(generics.ListAPIView):

    queryset = Payments.objects.all().order_by('-pid')
    serializer_class = PaymentSerializer


class StageViewAPI(generics.ListCreateAPIView):

    queryset = Stages.objects.all().order_by('-sid')
    serializer_class = StagesSerializer


class ChallansAPI(generics.ListCreateAPIView):
    
    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializer

    def get_queryset(self, *args, **kwargs):
        return super(ChallansAPI, self).get_queryset(*args, **kwargs)\
            .annotate(no_assign_order=models.Count('midorder'))\
                .filter(no_assign_order__gt=0).filter(~models.Q(midorder__isDone = False))


class MyJobsApi(generics.ListAPIView):

    queryset = Jobs.objects.all().order_by('-jid')
    serializer_class = JobSerializerWithStatus
