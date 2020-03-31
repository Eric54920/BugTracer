from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tracer/', include(("tracer.urls", "tracer"), namespace="tracer")),
    url(r'^', include(("web.urls", "web"), namespace="web")),
]