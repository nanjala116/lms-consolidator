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

# The first argument is the URL prefix, and the second argument is the viewset class
# This will create the following URL patterns:
# - /api/research_groups/ (list and create)
# - /api/research_groups/{id}/ (retrieve, update, partial update, destroy)
# - /api/research_groups/{id}/{custom_action}/ (for any custom actions defined in the viewset)
router.register(r'research_groups', ResearchGroupViewSet)

# Register the MOOChub-compatible viewset with a different URL prefix
# This creates a separate API endpoint specifically formatted for MOOChub
# - /api/moochub/organizations/ (list only)
# - /api/moochub/organizations/{id}/ (retrieve only)
router.register(r'moochub/organizations', MOOChubOrganizationViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
