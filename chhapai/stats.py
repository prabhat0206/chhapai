from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from datetime import date


class HomePageTopStatus(ListAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializer

    def get(self, request):
        instance = self.get_queryset()
        pending_jobs = instance.annotate(no_assign_order=models.Count('midorder'))\
            .filter(no_assign_order=0).count()
        processing_jobs = instance.annotate(no_assign_order=models.Count('midorder'))\
                .filter(no_assign_order__gt=0).filter(isCompleted=False).count()
        late_job = instance.filter(isCompleted=False).filter(comitted_date__lt = date.today()).count()
        payments = instance.annotate(no_assign_order=models.Count('payments'))\
            .filter(no_assign_order=0)
        pending_payments = payments.count()
        pending_payment_amount = payments.aggregate(models.Sum('payments')).get('payments__sum')
        pending_delivery = instance.filter(isDelivered=False).count()
        on_hold = instance.filter(isOnHold=True).count()

        res_dic = {
            "pending_jobs": pending_jobs,
            "processing_jobs": processing_jobs,
            "late_job": late_job,
            "pending_payments": pending_payments,
            "pending_payment_amount": pending_payment_amount,
            "pending_delivery": pending_delivery,
            "on_hold": on_hold
        }

        return Response({"Success": True, "Stats": res_dic})


class Last5Details(ListAPIView):

    queryset = Orders.objects.all().order_by("-oid")
    serializer_class = OrderSerializer

    def get(self, request):

        orders = OrderSerializer(self.get_queryset()[:5], many=True).data
        jobs = JobSerializer(Jobs.objects.all().order_by('-jid')[:5], many=True).data
        for_deliver_today = JobSerializer(Jobs.objects.all().order_by('-jid').filter(comitted_date = date.today())[:5], many=True).data
        last5 = {
            "orders": orders,
            "jobs": jobs,
            "for_deliver_today": for_deliver_today
        }
        return Response({"Success": True, "last5": last5})
        

class JobInEachStage(ListAPIView):

    queryset = Stages.objects.all()
    serializer_class = StagesSerializerWithCount


