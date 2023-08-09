from django.urls import path
from .views import CwEncryption
from .views import CwDcryption

urlpatterns = [
    path('encryption', CwEncryption.as_view(), name='fetch-cw-data'),
    path('v1/<str:data>/', CwDcryption.as_view(), name='fetch-cw'),
]