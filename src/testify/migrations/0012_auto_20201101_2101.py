# Generated by Django 3.1 on 2020-11-01 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testify', '0011_userresponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='write_date',
        ),
    ]
