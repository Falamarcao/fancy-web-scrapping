# Generated by Django 4.0.6 on 2023-01-12 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='Name')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Address')),
                ('url', models.URLField(null=True, verbose_name='URL')),
            ],
        ),
    ]
