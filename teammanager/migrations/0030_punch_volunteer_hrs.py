# Generated by Django 2.2.4 on 2019-09-25 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teammanager', '0029_auto_20190903_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='punch',
            name='volunteer_hrs',
            field=models.IntegerField(default=0),
        ),
    ]