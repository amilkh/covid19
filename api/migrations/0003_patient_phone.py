# Generated by Django 3.0.4 on 2020-03-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200316_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
    ]