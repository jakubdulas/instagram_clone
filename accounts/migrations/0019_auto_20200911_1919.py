# Generated by Django 3.0.8 on 2020-09-11 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20200911_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='date_posted',
        ),
    ]
