# Generated by Django 3.0.8 on 2020-09-11 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200911_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['id']},
        ),
    ]
