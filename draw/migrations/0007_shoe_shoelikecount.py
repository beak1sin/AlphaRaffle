# Generated by Django 4.0.3 on 2023-05-13 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0006_shoelike_remove_shoe_likes_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='shoelikecount',
            field=models.IntegerField(default=0),
        ),
    ]
