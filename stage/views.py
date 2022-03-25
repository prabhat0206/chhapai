from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chhapai.models import *
from django.db.models import Q
from .serializer import MidOrderWithPermission


class UserViewByPermissions(generics.ListAPIView):

    queryset = MidOrder.objects.all()
    serializer_class = MidOrderWithPermission
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_queryset().filter(isDone=False)\
            .filter(stage__in=user.groups.all())\
            .filter(Q(assigned_staff=request.user) | Q(assigned_staff=None))
        serialized = self.serializer_class(instance, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)
