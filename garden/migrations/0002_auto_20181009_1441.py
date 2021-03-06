# Generated by Django 2.1.1 on 2018-10-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gardengroup',
            name='short_name',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gardengroup',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='organisation',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
