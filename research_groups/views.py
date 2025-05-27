from django.shortcuts import render, get_object_or_404
from .models import ResearchGroup

def researchgroup_list(request):
    view_mode = request.GET.get('view', 'block')
    groups = ResearchGroup.objects.all()
    return render(request, 'research_groups/research_groups_list.html', {
        'groups': groups,
        'view_mode': view_mode,
    })

def researchgroup_detail(request, pk):
    group = get_object_or_404(ResearchGroup, pk=pk)
    return render(request, 'research_groups/research_group_detail.html', {'group': group})