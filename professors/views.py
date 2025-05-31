from django.shortcuts import render, get_object_or_404
from .models import Professor

def professor_list(request):
    view_mode = request.GET.get('view', 'block')
    professors = Professor.objects.all()
    return render(request, 'professors/professors_list.html', {
        'professors': professors,
        'view_mode': view_mode,
    })

def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    return render(request, 'professors/professor_detail.html', {'professor': professor})