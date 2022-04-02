from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

def home(request):
    return JsonResponse({"Success": True}, safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('chhapai.urls')),
    path('vendor/', include('staff.urls')),
    path('rest/', include('stage.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
