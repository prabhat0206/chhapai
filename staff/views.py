from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from chhapai.models import *
from chhapai.serializer import *
from .serializer import *


class AddOrderAPi(generics.CreateAPIView):

    queryset = Orders.objects.all()
    serializer_class = OrderSerializerVendor
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        new_order = self.serializer_class(data=request.data)
        if new_order.is_valid():
            new_order.save()
            for product in request.data.get('jobs'):
                product['order'] = new_order.data['oid']
                jobs = JobSerializerVendor(data=product)
                if jobs.is_valid():
                    jobs.save()
            return Response({"Success": True})
        return Response({"Success": False})


class AssignOrderJob(generics.CreateAPIView):
    
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderVerndorSerializer
    permission_classes = [AllowAny, ]

