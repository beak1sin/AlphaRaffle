# Generated by Django 4.0.3 on 2023-12-02 15:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0011_deletionreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='category',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='shoe',
            name='kream_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='shoe',
            name='product_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='shoe',
            name='soldout_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('comfort', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('size_fit', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='draw.shoe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='draw.member')),
            ],
        ),
    ]
