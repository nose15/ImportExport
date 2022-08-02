# Generated by Django 4.0.6 on 2022-08-02 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_package_route_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='state',
            field=models.CharField(choices=[('Registered', 'Registered'), ('En Route', 'En Route'), ('Delivered', 'Delivered'), ('At warehouse', 'At warehouse'), ('Delivery Confirmed', 'Delivery Confirmed')], default='Registered', max_length=60),
        ),
        migrations.AlterField(
            model_name='packagestatetransitions',
            name='state',
            field=models.CharField(choices=[('Registered', 'Registered'), ('En Route', 'En Route'), ('Delivered', 'Delivered'), ('At warehouse', 'At warehouse'), ('Delivery Confirmed', 'Delivery Confirmed')], default='Registered', max_length=60),
        ),
        migrations.CreateModel(
            name='WarehouseManagerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.warehouse')),
            ],
        ),
    ]
