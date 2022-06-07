from django.urls import path

from .views import *

urlpatterns = [
    path('info_log/', BasicItemInformationView.as_view()),
    path('detail_log/', ItemInstanceView.as_view()),
]