# Generated by Django 2.2.2 on 2019-07-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teammanager', '0002_auto_20190628_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('stu', 'Student'), ('mtr', 'Adult')], default='stu', max_length=10),
        ),
    ]