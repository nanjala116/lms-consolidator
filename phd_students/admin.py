import csv
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import PhDStudent
from core.admin_forms import CsvImportForm
from research_groups.models import ResearchGroup
from professors.models import Professor

@admin.register(PhDStudent)
class PhDStudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'research_group', 'supervisor']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='phd_students_phdstudent_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                count = 0
                for row in reader:
                    research_group = ResearchGroup.objects.get(name=row['research_group']) if row.get('research_group') else None
                    supervisor = Professor.objects.get(name=row['supervisor']) if row.get('supervisor') else None
                    PhDStudent.objects.create(
                        name=row['name'],
                        title=row['title'],
                        research_group=research_group,
                        supervisor=supervisor,
                        enrollment_date=row['enrollment_date'],
                        image_url=row['image_url'],
                    )
                    count += 1
                self.message_user(request, f"Imported {count} PhD students.", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = dict(self.admin_site.each_context(request), form=form, title="Import PhD Students from CSV")
        return render(request, "admin/csv_form.html", context)