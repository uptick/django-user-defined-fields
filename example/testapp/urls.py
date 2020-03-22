from django.conf.urls import include, url
from django.contrib import admin

from .views import TestDashboardView

urlpatterns = [
    url(r'^$', TestDashboardView.as_view(), name="start"),
    url('admin/', include(admin.site.urls)),
]
