# Generated by Django 3.1 on 2021-01-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210113_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.SmallIntegerField(null=True, verbose_name='Возраст'),
        ),
    ]
