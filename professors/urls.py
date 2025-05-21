from django.urls import path
from .views import (
    ProfessorListView, ProfessorDetailView, 
    CourseListView, CourseDetailView, 
    PhDStudentListView, PhDStudentDetailView, 
    ResearchGroupListView, ResearchGroupDetailView
)

urlpatterns = [
    # Professor views
    path("professors/", ProfessorListView.as_view(), name="professor_list"),
    path("professor/<int:pk>/", ProfessorDetailView.as_view(), name="professor_detail"),
    
    # Course views
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    
    # PhD Students views
    path("phd-students/", PhDStudentListView.as_view(), name="phd_student_list"),
    path("phd-student/<int:pk>/", PhDStudentDetailView.as_view(), name="phd_student_detail"),
    
    # Research Groups views
    path("research-groups/", ResearchGroupListView.as_view(), name="research_group_list"),
    path("research-group/<int:pk>/", ResearchGroupDetailView.as_view(), name="research_group_detail"),
]
