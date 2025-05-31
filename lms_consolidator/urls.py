from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Root URL handled by core.urls
    path('professors/', include('professors.urls')),
    path('courses/', include('courses.urls')),
    path('phd_students/', include('phd_students.urls')),
    path('research-groups/', include('research_groups.urls')),
    path('', views.home, name='home'),
]