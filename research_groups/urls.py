from django.urls import path
from . import views

urlpatterns = [
    path('', views.researchgroup_list, name='researchgroup_list'),
    path('<int:pk>/', views.researchgroup_detail, name='researchgroup_detail'),
]