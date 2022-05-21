from ast import Is
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
from django.utils import timezone
from staff.models import User
from datetime import datetime, timedelta
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class LoginToken(ObtainAuthToken):

    def post(self, request):
        serialized = self.serializer_class(
            data=request.data, context={'request': request})
        if serialized.is_valid():
            user = serialized.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            serialized_user = UserSerializer(user).data
            serialized_user['permissions'] = dict()
            groups = Group.objects.all()
            for group in groups:
                if group.name != "admin":
                    if group in user.groups.all():
                        serialized_user['permissions'][group.name] = True
                    else:
                        serialized_user['permissions'][group.name] = False
            del serialized_user["groups"]
            return Response({"Success": True, "token": token.key, "user": serialized_user})
        return Response({"Success": False, "Error": "Invalid login credentials"})


class UserStaffView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        return Response({'results': self.serializer_class(data, many=True).data})


class OverseerView(generics.ListAPIView):
    queryset = User.objects.all().filter(staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


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
        if request.user.superuser:
            instance = self.get_object()
        else:
            instance = request.user
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
    permission_classes = [IsAdminUser, ]

    def post(self, request, pk):
        instance = self.get_queryset().get(jid=pk)
        data_for_change = request._request.POST.dict()
        data_for_change['design'] = request._request.FILES.get('design')
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            midorder_sets = json.loads(data_for_change['midorders'])
            stage_ids = []
            for stage_id in midorder_sets:
                stage_ids.append(stage_id['stage'])
            stages = Group.objects.filter(id__in=stage_ids)
            if stages[0].midorder_set.last():
                if stages[0].midorder_set.last().expected_start_datetime > timezone.localtime(timezone.now()):
                    start_time = stages[0].midorder_set.last().expected_start_datetime
                else:
                    start_time = timezone.localtime(timezone.now())
            else:
                start_time = timezone.localtime(timezone.now())
            for midorder in midorder_sets:
                midorder['job'] = pk
                stage_time = stages.get(id=midorder['stage']).groupextension.completion_time
                expected_start_datetime = start_time + timedelta(minutes=stage_time)
                midorder['expected_start_datetime'] = expected_start_datetime
                if 'expected_complete_datetime' not in midorder:
                    midorder['expected_complete_datetime'] = expected_start_datetime + timedelta(minutes=stage_time)
                new_midorder = MidOrderVerndorSerializer(data=midorder)
                if new_midorder.is_valid():
                    new_midorder.save()
                    start_time = expected_start_datetime
                else:
                    return Response({"Success": False, "Error": new_midorder.errors})
            return Response({"Success": True})
        return {"Success": False, "Error": str(serialized.errors)}


class JobUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = Jobs.objects.all()
    serializer_class = JobSerializerWithOrderDetails
    permission_classes = [IsAuthenticated]


class MidOrderUpdateDestroyAPI(PartialUpdateDestroyView):

    queryset = MidOrder.objects.all()
    serializer_class = MidOrderVerndorSerializer


class AddGroupAPI(generics.CreateAPIView):

    queryset = Group.objects.all()
    serializer_class = AddStage
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save()
            request.data['groupextension']['group'] = serialized.data['id']
            extension = GroupExtensionSerializer(
                data=request.data['groupextension'])
            if extension.is_valid():
                extension.save()
            return Response({"Success": True, "Stage": serialized.data})
        return Response({"Success": True, "Error": serialized.errors})


class DeleteGroupAPI(PartialUpdateDestroyView):

    queryset = Group.objects.all()
    serializer_class = AddStage
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

    def post(self, request):
        data = request.data
        data['generated_by'] = request.user.id
        serilized_data = self.serializer_class(data=data)
        if serilized_data.is_valid():
            serilized_data.save()
            return Response({"Success": True, "Challan": serilized_data.data})
        return Response({"Success": False, "Errors": serilized_data.errors})


class ChallanUpdateDistroy(PartialUpdateDestroyView):
    queryset = Challans.objects.all()
    serializer_class = ChallanSerializer
    permission_classes = [IsAdminUser]


class CreatePaymentApi(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]


class OrderTypeCreate(generics.CreateAPIView):
    queryset = OrderType
    serializer_class = OrderTypeSerializer
    permission_classes = [IsAdminUser]