# Generated by Django 4.0.6 on 2022-07-30 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_package_reciever_id_alter_package_sender_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='reciever_id',
        ),
        migrations.RemoveField(
            model_name='package',
            name='sender_id',
        ),
        migrations.AddField(
            model_name='package',
            name='receiver_email',
            field=models.EmailField(default='dupablada@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='sender_email',
            field=models.EmailField(default='jajobyka@wp.pl', max_length=254),
            preserve_default=False,
        ),
    ]
