# Generated by Django 4.0.6 on 2022-08-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_package_state_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='busy',
        ),
        migrations.AddField(
            model_name='car',
            name='type',
            field=models.CharField(choices=[('van', 'van'), ('truck', 'truck')], default='van', max_length=10),
        ),
    ]
