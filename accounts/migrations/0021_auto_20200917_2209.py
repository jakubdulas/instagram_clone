# Generated by Django 3.0.8 on 2020-09-17 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20200915_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='comment_body',
        ),
    ]