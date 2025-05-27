from django.urls import path
from . import views

urlpatterns = [
    path('', views.professor_list, name='professor_list'),
    path('<int:pk>/', views.professor_detail, name='professor_detail'),
]