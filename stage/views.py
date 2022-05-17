from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chhapai.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from chhapai.serializer import UserSerializerWithGroup
from .serializer import MidOrderWithPermission


class UserViewByPermissions(generics.ListAPIView):

    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithPermission
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_queryset().filter(isDone=False)\
            .filter(stage__in=user.groups.all())\
            .filter(expected_start_datetime__lte=datetime.now())\
            .filter(Q(assigned_staff=request.user) | Q(assigned_staff=None))
        serialized = self.serializer_class(instance, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


class UpcomingJobsUser(generics.ListAPIView):
    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithPermission
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_queryset().filter(isDone=False)\
            .filter(stage__in=user.groups.all())\
            .filter(expected_start_datetime__gt=datetime.now())\
            .filter(Q(assigned_staff=request.user) | Q(assigned_staff=None))
        serialized = self.serializer_class(instance, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


class EditProfile(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerWithGroup
    permission_classes = [IsAuthenticated]

    def update(self, request, pk):
        instance = request.user
        data_for_change = request.data
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            return Response({"Success": True, "data": serialized.data})
        return Response({"Success": False, "Errors": str(serialized.errors)})
