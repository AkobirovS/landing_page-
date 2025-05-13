from django.urls import path
from landing.views import LeadCreateView

urlpatterns = [
    path('lead/', LeadCreateView.as_view(), name='lead-create'),
]
