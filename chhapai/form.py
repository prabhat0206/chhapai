from django.forms import ModelForm
from .models import *

class JobForm(ModelForm):

    class Meta:
        model = Jobs
        fields = ['job_name', 'notes', 'design', 'isEmailing',
                  'overseer', 'comitted_date', 'order_type']

