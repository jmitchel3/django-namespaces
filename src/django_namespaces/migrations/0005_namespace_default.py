# Generated by Django 4.1.6 on 2023-03-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_namespaces', '0004_alter_namespace_options_rename_slug_namespace_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='namespace',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
