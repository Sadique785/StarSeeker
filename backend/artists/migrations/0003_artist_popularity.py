# Generated by Django 5.2 on 2025-04-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_newartist'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]
