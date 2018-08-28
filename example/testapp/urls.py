from django.conf.urls import url
from django.contrib import admin

from .views import TestDashboardView

urlpatterns = [
    url(r'^$', TestDashboardView.as_view(), name="start"),
]
