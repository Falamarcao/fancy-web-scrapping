# Generated by Django 4.0.6 on 2023-01-05 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('name', models.CharField(max_length=140, verbose_name='Name')),
                ('description', models.CharField(max_length=140, verbose_name='Description')),
                ('duration', models.CharField(max_length=10, verbose_name='Duration')),
                ('sessions', models.JSONField(null=True, verbose_name='Sessions')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_movie', to='places.place', verbose_name='Place')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_movie', to='sources.source', verbose_name='Source')),
            ],
            options={
                'unique_together': {('source', 'place', 'name')},
            },
        ),
    ]
