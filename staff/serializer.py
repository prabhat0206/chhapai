from rest_framework import serializers
from chhapai.models import *
from django.contrib.auth.models import Group


class MidOrderVerndorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MidOrder
        fields = '__all__'

