# Generated by Django 4.0.3 on 2023-11-02 17:31

from django.db import migrations, models
import draw.models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0008_alter_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='avifimage',
            field=models.FileField(blank=True, help_text='.avif만 업로드 가능', null=True, upload_to='bannerimg/', validators=[draw.models.validate_avif_extension]),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, help_text='.png .jpeg .jpg .gif .svg만 업로드 가능', null=True, upload_to='bannerimg/', validators=[draw.models.validate_image_extension]),
        ),
    ]
