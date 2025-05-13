from django.urls import path
from .views import LeadCreateView

urlpatterns = [
    path('create-lead/', LeadCreateView.as_view(), name='create-lead'),
]
