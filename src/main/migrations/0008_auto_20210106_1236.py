# Generated by Django 3.1 on 2021-01-06 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210106_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='pics/fi1.jpg', upload_to='pics/'),
        ),
    ]
