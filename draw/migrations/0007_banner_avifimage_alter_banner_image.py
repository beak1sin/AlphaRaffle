# Generated by Django 4.0.3 on 2023-11-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0006_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='avifimage',
            field=models.FileField(blank=True, null=True, upload_to='bannerimgavif/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bannerimg/'),
        ),
    ]
