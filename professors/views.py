from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Professor, Course, PhDStudent, ResearchGroup

# List views for each model which allow searching

class ProfessorListView(ListView):
    model = Professor
    template_name = "professors_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Professor.objects.filter(name__icontains=query)
        return Professor.objects.all()

class CourseListView(ListView):
    model = Course
    template_name = "courses_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Course.objects.filter(title__icontains=query)
        return Course.objects.all()

class PhDStudentListView(ListView):
    model = PhDStudent
    template_name = "phdstudents_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return PhDStudent.objects.filter(name__icontains=query)
        return PhDStudent.objects.all()

class ResearchGroupListView(ListView):
    model = ResearchGroup
    template_name = "researchgroups_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return ResearchGroup.objects.filter(name__icontains=query)
        return ResearchGroup.objects.all()

# Detail views for each model

class ProfessorDetailView(DetailView):
    model = Professor
    template_name = "professor_detail.html"

class CourseDetailView(DetailView):
    model = Course
    template_name = "course_detail.html"

class PhDStudentDetailView(DetailView):
    model = PhDStudent
    template_name = "phdstudent_detail.html"

class ResearchGroupDetailView(DetailView):
    model = ResearchGroup
    template_name = "researchgroup_detail.html"
