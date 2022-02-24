from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class StagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stages
        fields = '__all__'


class MidOrderSerializer(serializers.ModelSerializer):
    stage = StagesSerializer()
    assigned_staff = UserSerializer()
    class Meta:
        model = MidOrder
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    midorder_set = MidOrderSerializer(many=True)
    class Meta:
        model = Jobs
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    jobs_set = JobSerializer(many=True)
    class Meta:
        model = Orders
        fields = '__all__'

