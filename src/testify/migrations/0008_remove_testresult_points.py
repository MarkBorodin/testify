# Generated by Django 3.1 on 2020-10-25 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testify', '0007_auto_20201023_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='points',
        ),
    ]
