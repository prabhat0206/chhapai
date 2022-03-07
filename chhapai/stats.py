from rest_framework.views import View
from .models import *


class HomePageTopStatus(View):

    def get(self, request):
        instance = Orders.object.all().order_by('-oid')
        pending_jobs = 0
