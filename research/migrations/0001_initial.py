# Generated by Django 4.2.7 on 2025-05-25 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('professors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('lead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='professors.professor')),
            ],
        ),
    ]
