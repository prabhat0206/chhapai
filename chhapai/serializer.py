from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', )
        extra_kwargs = {'password': {'write_only': True}}


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


class JobSerializerWithMid(serializers.ModelSerializer):
    midorder_set = MidOrderSerializer(many=True)
    class Meta:
        model = Jobs
        fields = '__all__'


class OrderSerializerWithJobs(serializers.ModelSerializer):
    jobs_set = JobSerializerWithMid(many=True)
    class Meta:
        model = Orders
        fields = '__all__'


class JobSerializerWithStatus(serializers.ModelSerializer):
    midorder_status = serializers.SerializerMethodField()
    class Meta:
        model = Jobs
        fields = '__all__'

    def get_midorder_status(self, instance):
        return MidOrderSerializer(instance.midorder_set.filter(isDone=False).first()).data


class OrderSerializerwithStatus(serializers.ModelSerializer):
    jobs_set = JobSerializerWithStatus(many=True)
    class Meta:
        model = Orders
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Jobs
        fields = '__all__'


class JobDetailsSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    midorder_set = MidOrderSerializer(many=True)

    class Meta:
        model = Jobs
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    class Meta:
        model = Payments
        fields = "__all__"


