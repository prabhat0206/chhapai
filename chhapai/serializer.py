from rest_framework import serializers
from .models import *
from staff.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from staff.serializer import GroupSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Jobs
        fields = '__all__'


class OrderTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderType
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        exclude = ['user_permissions']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializerWithGroup(UserSerializer):
    groups = GroupSerializer(many=True)


class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['permissions']
    

class StagesSerializerWithCount(StagesSerializer):
    jobs = serializers.SerializerMethodField()
    
    def get_jobs(self, instance):
        return instance.midorder_set.filter(isDone=False).count()


class MidOrderSerializer(serializers.ModelSerializer):
    stage = StagesSerializer()
    assigned_staff = UserSerializer()
    class Meta:
        model = MidOrder
        fields = '__all__'


class JobSerializerWithMid(JobSerializer):
    midorder_set = MidOrderSerializer(many=True)
    order_type = OrderTypeSerializer()


class OrderSerializerWithJobs(OrderSerializer):
    jobs_set = JobSerializerWithMid(many=True)


class JobSerializerWithStatus(JobSerializer):
    midorder_status = serializers.SerializerMethodField()

    def get_midorder_status(self, instance):
        return MidOrderSerializer(instance.midorder_set.filter(isDone=False).first()).data


class OrderSerializerwithStatus(OrderSerializer):
    jobs_set = JobSerializerWithStatus(many=True)


class JobDetailsSerializer(JobSerializer):
    order = OrderSerializer()
    midorder_set = MidOrderSerializer(many=True)


class PaymentSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    class Meta:
        model = Payments
        fields = "__all__"


class ChallanSerializer(serializers.ModelSerializer):
    job = JobDetailsSerializer()

    class Meta:
        model = Challans
        fields = '__all__'
