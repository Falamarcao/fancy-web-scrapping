# Generated by Django 4.0.6 on 2023-01-03 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=140, verbose_name='Name')),
                ('url', models.URLField(verbose_name='URL')),
            ],
        ),
    ]
