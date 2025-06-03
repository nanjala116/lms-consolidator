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

# The first argument is the URL prefix, and the second argument is the viewset class
# This will create the following URL patterns:
# - /api/phd_students/ (list and create)
# - /api/phd_students/{id}/ (retrieve, update, partial update, destroy)
# - /api/phd_students/{id}/{custom_action}/ (for any custom actions defined in the viewset)
router.register(r'phd_students', PhDStudentViewSet)

# Register the MOOChub-compatible viewset with a different URL prefix
# This creates a separate API endpoint specifically formatted for MOOChub
# - /api/moochub/students/ (list only)
# - /api/moochub/students/{id}/ (retrieve only)
router.register(r'moochub/students', MOOChubPhDStudentViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
