# Generated by Django 2.2.1 on 2019-06-01 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(
                    choices=[('build', 'Build Meeting'), ('out', 'Outreach'), ('comp', 'Competition'),
                             ('fun', 'Fun Event'), ('othr', 'Other Mandatory')], default='build', max_length=10)),
                ('name', models.TextField(blank=True, null=True)),
                ('signup_active', models.BooleanField()),
                ('self_register', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.TextField()),
                ('last', models.TextField()),
                ('role',
                 models.CharField(choices=[('stu', 'Student'), ('mtr', 'Mentor'), ('vol', 'Volunteer')], default='stu',
                                  max_length=10)),
                ('avatar', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teammanager.Meeting')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teammanager.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Punch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teammanager.Meeting')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teammanager.Member')),
            ],
        ),
    ]
