# Generated by Django 3.0.1 on 2020-01-13 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200112_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='labappointment',
            name='test_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.LabTest'),
        ),
    ]
