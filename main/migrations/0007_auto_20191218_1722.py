# Generated by Django 3.0 on 2019-12-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_doctor_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='addmission',
            new_name='admission',
        ),
        migrations.AlterField(
            model_name='service',
            name='picture',
            field=models.ImageField(upload_to='static'),
        ),
    ]
