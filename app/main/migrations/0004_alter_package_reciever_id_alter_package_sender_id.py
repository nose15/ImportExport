# Generated by Django 4.0.6 on 2022-07-30 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_package_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='reciever_id',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'groups__name': 'Customers'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Recievers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='sender_id',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'groups__name': 'Customers'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Senders', to=settings.AUTH_USER_MODEL),
        ),
    ]
