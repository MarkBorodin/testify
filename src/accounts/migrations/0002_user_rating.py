# Generated by Django 3.1 on 2020-10-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]