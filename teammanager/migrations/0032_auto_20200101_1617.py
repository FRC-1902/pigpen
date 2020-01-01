# Generated by Django 2.2.9 on 2020-01-01 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teammanager', '0031_auto_20191023_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='category',
            field=models.CharField(choices=[('stoff', 'Student Officers'), ('adbod', 'Adult Board of Directors'), ('stsub', 'Student Robot Leads'), ('adsub', 'Adult Robot Leads'), ('stbus', 'Student Business Leads'), ('adbus', 'Adult Business Leads'), ('old', 'People to Know')], max_length=10),
        ),
    ]
