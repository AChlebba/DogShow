# Generated by Django 4.0.6 on 2022-08-10 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_show_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
