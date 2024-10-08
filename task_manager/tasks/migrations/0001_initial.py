# Generated by Django 5.1 on 2024-08-23 18:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator_id', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executor_id', to=settings.AUTH_USER_MODEL, verbose_name='Executor')),
                ('labels', models.ManyToManyField(blank=True, null=True, related_name='labels', to='labels.label', verbose_name='Labels')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status', verbose_name='Status')),
            ],
        ),
    ]
