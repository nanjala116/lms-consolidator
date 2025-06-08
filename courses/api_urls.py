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

# Register the CourseViewSet with the basename 'course'
router.register(r'courses', CourseViewSet, basename='course')

# Register the MOOChubCourseViewSet with a unique basename to avoid conflicts
router.register(r'moochub/courses', MOOChubCourseViewSet, basename='moochub-course')

urlpatterns = [
    path('', include(router.urls)),
]
