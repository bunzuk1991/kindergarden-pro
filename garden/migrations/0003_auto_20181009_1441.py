# Generated by Django 2.1.1 on 2018-10-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0002_auto_20181009_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gardengroup',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]