from django.conf.urls import url
from .views import account, home

urlpatterns = [
    url(r'^send/sms/', account.send_sms, name="send_sms"),
    url(r'^register/$', account.register, name="register"),
    url(r'^login/sms/$', account.login_sms, name="login_sms"),
    url(r'^login/$', account.login, name="login"),
    url(r'^image/code/$', account.image_code, name='image_code'),
    url(r'^logout/$', account.logout, name="logout"),
    url(r'^index/$', home.index, name="index"),
    url(r'^manage/$', home.manage, name="manage"),
    url(r'^project/create/$', home.create_project, name="create_project"),
    url(r'^star/$', home.star, name="star"),
]