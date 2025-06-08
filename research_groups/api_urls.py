"""
URL configuration for the Research Groups app API.

This file defines the URL patterns for the research_groups API endpoints,
using Django REST Framework's router system to automatically generate
the appropriate URL patterns for the ResearchGroupViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import ResearchGroupViewSet, MOOChubOrganizationViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register the ResearchGroupViewSet with an explicit basename to avoid conflicts
router.register(r'research_groups', ResearchGroupViewSet, basename='researchgroup-api')

# Register the MOOChub-compatible viewset with a different URL prefix and basename
router.register(r'moochub/organizations', MOOChubOrganizationViewSet, basename='moochub-organization')

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
