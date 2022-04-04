from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from chhapai.models import *
from rest_framework.parsers import FormParser, MultiPartParser
from chhapai.serializer import *
import json
from .serializer import *
from chhapai.serializer import UserSerializer, UserSerializerWithGroup
from django.contrib.auth.models import Group
from staff.models import User


class UserStaffView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        return Response({'results': self.serializer_class(data, many=True).data})


class PartialUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, pk):
        instance = self.get_object()
        data_for_change = request.data
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            return Response({"Success": True, "data": serialized.data})
        return Response({"Success": False, "Errors": str(serialized.errors)})


class UserUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    response_serializer = UserSerializerWithGroup

    def update(self, request, pk):
        instance = self.get_object()
        data_for_change = request.data
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            user = self.get_object()
            if 'groups' in request.data:
                for group in user.groups.all():
                    group.user_set.remove(user)
                for group in request.data['groups']:
                    instance = Group.objects.get(id=group)
                    instance.user_set.add(user)
            return Response({"Success": True, "data": self.response_serializer(self.get_object()).data})
        return Response({"Success": False, "Errors": str(serialized.errors)})


class UserAddView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def post(self, request, *args, **kwargs):
        new_user = self.serializer_class(data=request.data)
        if new_user.is_valid():
            new_user.save()
            user = User.objects.get(id=new_user.data['id'])
            for group in request.data['groups']:
                instance = Group.objects.get(id=group)
                instance.user_set.add(user)
            return Response({"Success": True, "user": UserSerializerWithGroup(user).data})
        return Response({"Success": False, "error": new_user.errors})


class AddOrderAPi(generics.CreateAPIView):

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        new_order = self.serializer_class(data=request.data)
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


class AssignOrderJob(generics.CreateAPIView, generics.UpdateAPIView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        instance = self.get_queryset().get(jid=pk)
        data_for_change = request._request.POST.dict()
        data_for_change['design'] = request._request.FILES.get('design')
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            for midorder_set in json.loads(data_for_change['midorders']):
                midorder_set['job'] = pk
                new_midorder = MidOrderVerndorSerializer(data=midorder_set)
                if new_midorder.is_valid():
                    new_midorder.save()
                else:
                    return Response({"Success": False, "Error": new_midorder.errors})
            return Response({"Success": True})
        return {"Success": False, "Error": str(serialized.errors)}


class JobUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithOrderDetails


class MidOrderUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = MidOrder.objects.all()
    serializer_class = MidOrderVerndorSerializer


class AddGroupAPI(generics.CreateAPIView):

    queryset = Group.objects.all()
    serializer_class = StagesSerializer
    permission_classes = [IsAdminUser, ]


class GetGroupsAPI(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = StagesSerializer
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        return Response({"Success": True, "Groups": self.serializer_class(self.get_queryset(), many=True).data})


class CreateChallanApi(generics.CreateAPIView):
    queryset = Challans.objects.all()
    serializer_class = ChallanSerializer


class ChallanUpdateDistroy(PartialUpdateDestroyView):
    queryset = Challans.objects.all()
    serializer_class = ChallanSerializer


class CreatePaymentApi(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['created_by'] = request.user.id
        serilized_data = self.serializer_class(data=data)
        if serilized_data.is_valid():
            serilized_data.save()
            return Response({"Success": True, "Payments": serilized_data.data})
        return Response({"Success": False, "Errors": serilized_data.errors})

class PaymentUpdateDistroy(PartialUpdateDestroyView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
