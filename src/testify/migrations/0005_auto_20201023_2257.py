# Generated by Django 3.1 on 2020-10-23 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testify', '0004_testresult_taken_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='taken_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
