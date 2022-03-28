from rest_framework import serializers
from .models import *
from staff.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from staff.serializer import GroupSerializer


class OrderTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderType
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        exclude = ('user_permissions')
        extra_kwargs = {'password': {'write_only': True}}


class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    

class StagesSerializerWithCount(serializers.ModelSerializer):
    jobs = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = '__all__'
    
    def get_jobs(self, instance):
        return instance.midorder_set.filter(isDone=False).count()


class MidOrderSerializer(serializers.ModelSerializer):
    stage = StagesSerializer()
    assigned_staff = UserSerializer()
    class Meta:
        model = MidOrder
        fields = '__all__'


class JobSerializerWithMid(serializers.ModelSerializer):
    midorder_set = MidOrderSerializer(many=True)
    order_type = OrderTypeSerializer()
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


