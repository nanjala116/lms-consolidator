import csv
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Professor
from core.admin_forms import CsvImportForm

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'position', 'picture_tag']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='professors_professor_import_csv'
            ),
        ]
        return custom_urls + urls

    def picture_tag(self, obj):
        if obj.image_url:
            # Change width/height as you like
            return format_html('<img src="{}" style="height:60px;width:auto;"/>', obj.image_url)
        return "-"
    picture_tag.short_description = "Picture"

    def changelist_view(self, request, extra_context=None):
        """
        Add CSV import link to the context for the changelist template.
        """
        if extra_context is None:
            extra_context = {}
        extra_context['csv_import_link'] = reverse('admin:professors_professor_import_csv')
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
                    Professor.objects.create(
                        name=row['name'],
                        title=row['title'],
                        position=row['position'],
                        bio=row.get('bio', ''),
                        image_url=row.get('image_url', ''),
                        # Add handling for FKs if needed
                    )
                    count += 1
                self.message_user(request, f"Imported {count} professors.", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = dict(self.admin_site.each_context(request), form=form, title="Import Professors from CSV")
        return render(request, "admin/csv_form.html", context)