# Generated by Django 4.0.6 on 2022-07-14 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='address',
            field=models.CharField(default='jakis adres', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='description',
            field=models.TextField(default='sample description'),
            preserve_default=False,
        ),
    ]
