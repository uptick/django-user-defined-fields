from django.urls import path

from . import views

urlpatterns = [
    path("", views.TestDashboardView.as_view(), name="index"),
]
