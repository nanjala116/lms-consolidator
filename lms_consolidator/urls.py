"""
Main URL configuration for the LMS Consolidator project.

This file defines the URL patterns for the entire project,
including both web interface and API endpoints for all apps.
"""

from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Core application (includes home page and other core functionality)
    path('', include('core.urls')),
    
    # Web interface URLs for each app
    path('professors/', include('professors.urls')),
    path('courses/', include('courses.urls')),
    path('phd-students/', include('phd_students.urls')),
    path('research-groups/', include('research_groups.urls')),
    
    # API endpoints
    path('api/', include([
        # Include all app API URLs
        path('', include('professors.api_urls')),
        path('', include('courses.api_urls')),
        path('', include('phd_students.api_urls')),
        path('', include('research_groups.api_urls')),
    ]))
]
