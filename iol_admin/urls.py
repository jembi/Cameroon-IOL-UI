"""iol_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from iol_admin.settings.common import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # url('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # url('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url('admin/', admin.site.urls),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
