# Generated by Django 2.2.3 on 2019-07-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teammanager', '0009_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='category',
            field=models.CharField(choices=[('stoff', 'Student Officers'), ('tmldr', 'Team Leadership'),
                                            ('adbod', 'Adult Board of Directors'),
                                            ('stsub', 'Student Subsystem/Subteam Leads'),
                                            ('adsub', 'Adult Subsystem/Subteam Leads'),
                                            ('stbus', 'Student Business Leads'), ('adbus', 'Adult Business Leads')],
                                   max_length=10),
        ),
    ]
