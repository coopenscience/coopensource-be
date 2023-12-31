# Generated by Django 4.2.6 on 2023-10-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_project_geographic_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='agency_sponsor',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='agency_sponsor_other',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='email',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='fields_of_science',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='geographic_scope',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='keywords',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='participant_age',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='participation_tasks',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_goals',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='scistarter',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.TextField(),
        ),
    ]
