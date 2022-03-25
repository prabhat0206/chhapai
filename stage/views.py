from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chhapai.models import *
from django.db.models import Q
from rest_framework.response import Response
from .serializer import JobWithPermission


class UserViewByPermissions(generics.ListAPIView):

    queryset = MidOrder.objects.all()
    serializer_class = JobWithPermission
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_queryset().filter(stage__in=[user.groups.all()])\
            .filter(Q(assigned_staff=request.user) | Q(assigned_staff=None))
        serialized = self.serializer_class(instance, many=True)
        paginate = self.paginate_queryset(serialized)
        return Response(self.get_paginated_response(paginate))
