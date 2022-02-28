from dataclasses import fields
from rest_framework import serializers
from chhapai.models import *


class MidOrderVerndorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MidOrder
        fields = '__all__'


class JobSerializerVendor(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = '__all__'


class OrderSerializerVendor(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'
