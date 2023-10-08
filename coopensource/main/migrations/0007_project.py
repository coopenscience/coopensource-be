# Generated by Django 4.2.6 on 2023-10-08 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_delete_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('project_url_on_catalog', models.URLField()),
                ('project_url_external', models.URLField()),
                ('project_description', models.TextField()),
                ('keywords', models.CharField(max_length=500)),
                ('fields_of_science', models.CharField(max_length=255)),
                ('project_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=50)),
                ('agency_sponsor', models.CharField(max_length=255)),
                ('agency_sponsor_other', models.CharField(blank=True, max_length=255)),
                ('geographic_scope', models.CharField(max_length=100)),
                ('participant_age', models.CharField(max_length=255)),
                ('project_goals', models.TextField(blank=True)),
                ('participation_tasks', models.CharField(max_length=500)),
                ('scistarter', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254)),
                ('start_date', models.DateField()),
            ],
        ),
    ]