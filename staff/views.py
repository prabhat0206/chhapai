from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chhapai.form import JobForm
from chhapai.models import *
from rest_framework.parsers import FormParser, MultiPartParser
from chhapai.serializer import *
import json
from .serializer import *
from chhapai.serializer import UserSerializer
from django.contrib.auth.models import User


class PartialUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        data_for_change = request.data
        serialized = self.serializer_class(instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            return Response({"Success": True, "data": serialized.data})
        return Response({"Success": False, "Errors": str(serialized.errors)})


class UserUpdateDestroyView(PartialUpdateDestroyView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAddView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated,]

    def update(self, request, pk):
        instance = self.get_queryset().get(id=pk)
        data_for_change = request._request.POST
        serialized = JobForm(request._request.POST, request._request.FILES ,instance=instance)
        if serialized.is_valid():
            serialized.save()
            for midorder_set in json.loads(data_for_change['midorders']):
                midorder_set['job'] = instance
                new_midorder = MidOrderVerndorSerializer(midorder_set)
                if new_midorder.is_valid():
                    new_midorder.save()
            return {"Success": True}
        return {"Success": False, "Error": str(serialized.errors)}


class JobUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializer


class MidOrderUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = MidOrder.objects.all()
    serializer_class = MidOrderVerndorSerializer

