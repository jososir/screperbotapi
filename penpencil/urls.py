from django.urls import path
from .views import FetchPenPencilData

urlpatterns = [
    path('', FetchPenPencilData.as_view(), name='fetch-penpencil-data'),
]