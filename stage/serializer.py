from rest_framework.serializers import ModelSerializer
from chhapai.models import Jobs, MidOrder


class JobWithPermission(ModelSerializer):
    
    class Meta:
        model = Jobs
        exclude = ('unit_cost', 'isDelivered', 'isEmailing', 'total_cost', 'notes', 'overseer')

class MidOrderWithPermission(ModelSerializer):
    job = JobWithPermission()
    class Meta:
        model = MidOrder
        fields = '__all__'

