# Generated by Django 4.0.3 on 2023-11-02 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0005_shoesite_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='bannerimg/')),
            ],
        ),
    ]
