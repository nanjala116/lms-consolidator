"""
URL configuration for the Courses app API.

This file defines the URL patterns for the courses API endpoints,
using Django REST Framework's router system to automatically generate
the appropriate URL patterns for the CourseViewSet and MOOChubCourseViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import CourseViewSet, MOOChubCourseViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# The first argument is the URL prefix, and the second argument is the viewset class
# This will create the following URL patterns:
# - /api/courses/ (list and create)
# - /api/courses/{id}/ (retrieve, update, partial update, destroy)
# - /api/courses/{id}/{custom_action}/ (for any custom actions defined in the viewset)
router.register(r'courses', CourseViewSet)

# Register the MOOChub-compatible viewset with a different URL prefix
# This creates a separate API endpoint specifically formatted for MOOChub
# - /api/moochub/courses/ (list only)
# - /api/moochub/courses/{id}/ (retrieve only)
router.register(r'moochub/courses', MOOChubCourseViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
]
