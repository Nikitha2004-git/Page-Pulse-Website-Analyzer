from django.urls import path
from .views import home, analyze_url
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("analyze/", analyze_url, name="analyze"),
       path("download-report/", views.download_report, name="download_report"),
]