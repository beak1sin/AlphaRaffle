# Generated by Django 4.0.3 on 2023-04-07 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0003_alter_comment_member_nickname_alter_comment_serialno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(db_column='created_date'),
        ),
    ]
