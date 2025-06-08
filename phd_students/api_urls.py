"""
URL configuration for the PhD Students app API.

This file defines the URL patterns for the phd_students API endpoints,
using Django REST Framework's router system to automatically generate
the appropriate URL patterns for the PhDStudentViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import PhDStudentViewSet, MOOChubPhDStudentViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register the PhDStudentViewSet with a unique basename to avoid conflicts
router.register(r'phd_students', PhDStudentViewSet, basename='phdstudent-api')

# Register the MOOChub-compatible viewset with a different URL prefix and unique basename
router.register(r'moochub/students', MOOChubPhDStudentViewSet, basename='moochub-phdstudent')

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
