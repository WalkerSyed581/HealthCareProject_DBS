# Generated by Django 3.0 on 2019-12-18 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191218_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportgroup',
            name='support_group_conductor',
        ),
        migrations.RemoveField(
            model_name='supportgroupconductor',
            name='conducts',
        ),
        migrations.AddField(
            model_name='supportgroup',
            name='conducted_by',
            field=models.ManyToManyField(null=True, to='main.SupportGroupConductor'),
        ),
    ]
