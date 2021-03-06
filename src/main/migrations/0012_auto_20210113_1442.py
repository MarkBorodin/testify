# Generated by Django 3.1 on 2021-01-13 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_auto_20210113_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='teacher',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='clients', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lessons',
            name='teacher',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='lessons', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='client',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='lessons', to='main.client'),
        ),
    ]
