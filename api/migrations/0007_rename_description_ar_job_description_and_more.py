# Generated by Django 4.0.5 on 2022-08-16 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_companyadmin_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='description_ar',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='job',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='job',
            name='description_fr',
        ),
    ]
