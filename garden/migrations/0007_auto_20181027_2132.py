# Generated by Django 2.1.1 on 2018-10-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0006_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
