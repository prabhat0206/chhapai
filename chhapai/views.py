from rest_framework import generics
from .models import *
from .serializer import *


class OrderView(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-oid')
    serializer_class = OrderSerializer



