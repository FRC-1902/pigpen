# Generated by Django 2.2.4 on 2019-08-08 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teammanager', '0025_punch_fake'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(
                choices=[('stu', 'Student'), ('mtr', 'Adult'), ('asib', 'Sibling'), ('vip', 'VIP Bacon')],
                default='stu', max_length=10),
        ),
    ]
