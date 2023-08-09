from django.urls import path
from .views import FetchTunkatunkaunData

urlpatterns = [
    path('', FetchTunkatunkaunData.as_view(), name='fetch-tunkatunka-data'),
]