import csv
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import ResearchGroup
from core.admin_forms import CsvImportForm

@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ['name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='research_groups_researchgroup_import_csv'),
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
                    ResearchGroup.objects.create(
                        name=row['name'],
                        description=row['description'],
                    )
                    count += 1
                self.message_user(request, f"Imported {count} research groups.", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = dict(self.admin_site.each_context(request), form=form, title="Import Research Groups from CSV")
        return render(request, "admin/csv_form.html", context)