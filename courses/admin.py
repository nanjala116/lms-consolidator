import csv
import io
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import Course
from core.admin_forms import CsvImportForm

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='courses_course_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                # Use utf-8-sig to handle BOM
                decoded_file = io.TextIOWrapper(csv_file, encoding='utf-8-sig')
                reader = csv.DictReader(decoded_file)

                count = 0
                for row in reader:
                    # Normalize headers and values: strip, lowercase, remove BOM and whitespace
                    row = {
                        k.strip().lower().replace('\ufeff', ''):
                        (v.strip().replace('\xa0', ' ') if isinstance(v, str) else v)
                        for k, v in row.items()
                    }
                    # Optionally, show row content in admin messages for debugging
                    # self.message_user(request, f"Row: {row}", messages.INFO)
                    Course.objects.create(
                        name=row.get('name', ''),
                        description=row.get('description', ''),
                        image_url=row.get('image_url', ''),
                        credits=row.get('credits') or None,
                        code=row.get('code', ''),
                        start_date=row.get('start_date') or None,
                        end_date=row.get('end_date') or None,
                        format=row.get('format', ''),
                        level=row.get('level', ''),
                    )
                    count += 1
                self.message_user(request, f"Imported {count} courses (incomplete data allowed).", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = dict(self.admin_site.each_context(request), form=form, title="Import Courses from CSV")
        return render(request, "admin/csv_form.html", context)