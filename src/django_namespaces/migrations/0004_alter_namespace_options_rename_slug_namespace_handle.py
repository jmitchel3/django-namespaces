# Generated by Django 4.1.6 on 2023-03-17 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_namespaces', '0003_alter_namespace_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='namespace',
            options={'ordering': ['handle', '-updated_at', '-created_at']},
        ),
        migrations.RenameField(
            model_name='namespace',
            old_name='slug',
            new_name='handle',
        ),
    ]