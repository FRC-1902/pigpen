# Generated by Django 2.2.3 on 2019-07-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teammanager', '0005_auto_20190717_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='attendance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='hours',
            field=models.IntegerField(default=0),
        ),
    ]
