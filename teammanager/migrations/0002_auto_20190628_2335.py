# Generated by Django 2.2.2 on 2019-06-28 23:35

from django.db import migrations, models

import teammanager.utils


class Migration(migrations.Migration):
    dependencies = [
        ('teammanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=teammanager.utils.gen_token, max_length=100)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='meeting',
            name='self_register',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='signup_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='punch',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='punch',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
