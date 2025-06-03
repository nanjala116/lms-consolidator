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

# The first argument is the URL prefix, and the second argument is the viewset class
# This will create the following URL patterns:
# - /api/professors/ (list and create)
# - /api/professors/{id}/ (retrieve, update, partial update, destroy)
# - /api/professors/{id}/{custom_action}/ (for any custom actions defined in the viewset)
router.register(r'professors', ProfessorViewSet)

# Register the MOOChub-compatible viewset with a different URL prefix
# This creates a separate API endpoint specifically formatted for MOOChub
# - /api/moochub/persons/ (list only)
# - /api/moochub/persons/{id}/ (retrieve only)
router.register(r'moochub/persons', MOOChubPersonViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
