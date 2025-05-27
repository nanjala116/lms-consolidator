from django.shortcuts import render, get_object_or_404
from .models import PhDStudent

def phdstudent_list(request):
    view_mode = request.GET.get('view', 'block')
    students = PhDStudent.objects.all()
    return render(request, 'phd_students/phd_students_list.html', {
        'students': students,
        'view_mode': view_mode,
    })

def phdstudent_detail(request, pk):
    student = get_object_or_404(PhDStudent, pk=pk)
    return render(request, 'phd_students/phd_student_detail.html', {'student': student})