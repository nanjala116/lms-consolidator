"""
URL configuration for the Professors app API.

This file defines the URL patterns for the professors API endpoints,
using Django REST Framework's router system to automatically generate
the appropriate URL patterns for the ProfessorViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import ProfessorViewSet, MOOChubPersonViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register the main ProfessorViewSet with the basename 'professor'
router.register(r'professors', ProfessorViewSet, basename='professor')

# Register the MOOChub-compatible viewset with a different basename to avoid conflicts
router.register(r'moochub/persons', MOOChubPersonViewSet, basename='moochub-person')

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
