# Generated by Django 4.0.3 on 2022-05-28 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0002_alter_userdata_options_alter_userdata_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='usernickname',
            field=models.CharField(max_length=200),
        ),
    ]
