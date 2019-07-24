# Generated by Django 2.2.3 on 2019-07-24 22:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teammanager', '0012_auto_20190723_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='self_register',
        ),
        migrations.AddField(
            model_name='meeting',
            name='members',
            field=models.ManyToManyField(to='teammanager.Member'),
        ),
    ]