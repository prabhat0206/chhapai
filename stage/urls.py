from django.urls import path
from .views import *

urlpatterns = [
    path('user_process_jobs', UserViewByPermissions.as_view(), name='user_jobs'),
    path('user_upcoming_jobs', UpcomingJobsUser.as_view(), name='user_up'),
    path('edit_profile/<int:pk>', EditProfile.as_view(), name='edit_')
]


