# Generated by Django 2.0.3 on 2018-06-14 11:03

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=32, verbose_name='Field group')),
                ('order', models.IntegerField(default=0)),
                ('label', models.CharField(max_length=50, verbose_name='Display name')),
                ('name', models.SlugField()),
                ('widget', models.CharField(choices=[('text', 'Text'), ('multiline-text', 'Multiline Text'), ('integer', 'Integer'), ('choice', 'Choice'), ('date', 'Date')], default='text', max_length=32)),
                ('default', models.CharField(blank=True, default='', max_length=1024)),
                ('in_list', models.BooleanField(default=True, verbose_name='Show in list view?')),
                ('required', models.BooleanField(default=False, verbose_name='Should field be required?')),
                ('help_text', models.CharField(blank=True, max_length=300)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
                ('field_settings', models.jsonb.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ('content_type', 'group', 'order'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='extrafield',
            unique_together={('content_type', 'name')},
        ),
        migrations.CreateModel(
            name='DisplayCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=32)),
                ('values', models.CharField(blank=True, max_length=200)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userdefinedfields.ExtraField'))
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
