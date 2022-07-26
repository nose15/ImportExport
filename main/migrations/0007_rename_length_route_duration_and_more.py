# Generated by Django 4.0.6 on 2022-08-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_package_current_warehouse_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='length',
            new_name='duration',
        ),
        migrations.RemoveField(
            model_name='route',
            name='destination_latitude',
        ),
        migrations.RemoveField(
            model_name='route',
            name='destination_longitude',
        ),
        migrations.RemoveField(
            model_name='route',
            name='interwarehouse',
        ),
        migrations.RemoveField(
            model_name='route',
            name='origin_latitude',
        ),
        migrations.RemoveField(
            model_name='route',
            name='origin_longitude',
        ),
        migrations.RemoveField(
            model_name='route',
            name='state',
        ),
        migrations.AddField(
            model_name='route',
            name='type',
            field=models.CharField(choices=[('InterWarehouse', 'InterWarehouse'), ('PickUp', 'PickUp'), ('Delivery', 'Delivery')], default='InterWarehouse', max_length=60),
            preserve_default=False,
        ),
    ]
