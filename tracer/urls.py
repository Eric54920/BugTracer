from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^send/sms/', views.send_sms),
    url(r'^register/', views.register),
    url(r'^upload/', views.upLoad),
]
