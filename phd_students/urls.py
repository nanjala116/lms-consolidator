from django.urls import path
from . import views

urlpatterns = [
    path('', views.phdstudent_list, name='phdstudent_list'),
    path('<int:pk>/', views.phdstudent_detail, name='phd_student_detail'),
]