# Generated by Django 3.2.25 on 2025-04-24 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlescore',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
