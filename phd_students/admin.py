import csv
from django.contrib import admin, messages
from django import forms
from django.shortcuts import render, redirect
from django.urls import path, reverse
from .models import PhDStudent
from core.admin_forms import CsvImportForm
from research_groups.models import ResearchGroup
from professors.models import Professor

# Custom admin form: only 'name' is required
class PhDStudentAdminForm(forms.ModelForm):
    class Meta:
        model = PhDStudent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'name':
                self.fields[field_name].required = False

@admin.register(PhDStudent)
class PhDStudentAdmin(admin.ModelAdmin):
    form = PhDStudentAdminForm
    list_display = ['name', 'title', 'research_group', 'supervisor']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='phd_students_phdstudent_import_csv'
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['csv_import_link'] = reverse('admin:phd_students_phdstudent_import_csv')
        return super().changelist_view(request, extra_context=extra_context)

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                count = 0
                for row in reader:
                    # Get related objects or set None if not found
                    research_group = None
                    supervisor = None
                    if row.get('research_group'):
                        try:
                            research_group = ResearchGroup.objects.get(name=row['research_group'])
                        except ResearchGroup.DoesNotExist:
                            research_group = None
                    if row.get('supervisor'):
                        try:
                            supervisor = Professor.objects.get(name=row['supervisor'])
                        except Professor.DoesNotExist:
                            supervisor = None
                    PhDStudent.objects.create(
                        name=row['name'],
                        title=row.get('title', ''),
                        research_group=research_group,
                        supervisor=supervisor,
                        enrollment_date=row.get('enrollment_date') or None,
                        image_url=row.get('image_url', ''),
                    )
                    count += 1
                self.message_user(request, f"Imported {count} PhD students.", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = dict(self.admin_site.each_context(request), form=form, title="Import PhD Students from CSV")
        return render(request, "admin/csv_form.html", context)