from django.shortcuts import render, get_object_or_404
from .models import Course

def course_list(request):
    view_mode = request.GET.get('view', 'block')
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {
        'courses': courses,
        'view_mode': view_mode,
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})